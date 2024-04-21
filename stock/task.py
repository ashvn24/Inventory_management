from datetime import timedelta
from io import BytesIO
import os
import random
from celery import shared_task
from django.conf import settings
from django.http import FileResponse, HttpResponse
import openpyxl
from .models import Order, CartOrder, Shipment, Product
from django.core.mail import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils import timezone
from openpyxl.styles import Alignment


@shared_task(bind=True)
def Check_cart(self,id):
    print(id)
    cart = CartOrder.objects.get(pk=id)
    if cart.quantity == cart.order.quantity:
        ship = Shipment.objects.create(
            ship_order =cart.order,
            status = True,
            tracking_number = random.randint(100000,999999),
            items =cart,
            address = cart.order.Address
        )
        ship.save()
        send_conformation(cart.order.email,cart.order.order_id,cart.order.Product)
    product = cart.product
    
    product.quantity -= cart.quantity
    product.save()
    
    
@shared_task
def CheckStock():
    print('hiiii--')
    product = Product.objects.filter(quantity__lte=5)
    for prod in product:
        send_mail.delay(prod.Name)
    

sender_email = settings.EMAIL_HOST_USER
receiver_mail = settings.EMAIL_HOST_RECIEVER
password = settings.EMAIL_HOST_PASSWORD

@shared_task(bind=True)
def send_mail(self, product):
    
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_mail
        msg['Subject'] = "Product is out of stock"
        body = f"Product {product} is out of stock"
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_mail, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            print('Failed to send email. Please check your email configuration.')


        
    
def send_conformation(email, id, product):
    
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Product Shipped"
        body = f"Your Order with order id:{id} of product:{product} is Shipped!"
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, email, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            print('Failed to send email. Please check your email configuration.')
            
@shared_task
def download_sales_report():
    generate_sales()
    
            
def generate_sales():
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    sales = Shipment.objects.filter(date_shipped__gte=thirty_days_ago)

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    
    headers = [
        "Order_id",
        "tracking_id",
        "Customer_Name",
        "Email",
        "Address",
        "Product",
        "Quantity",
        "Price/Item",
        "Total"
    ]
    worksheet.append(headers)
    
    for sale in sales:
        ord = sale.ship_order.order_id
        track = sale.tracking_number
        customer = sale.ship_order.Name
        email = sale.ship_order.email
        addr = sale.ship_order.Address
        prod = sale.ship_order.Product.Name
        qnty = sale.items.quantity
        price = sale.ship_order.Product.price
        total = round(qnty * price, 2)
        
        row_data = [
            ord,
            track,
            customer,
            email,
            addr,
            prod,
            qnty,
            price,
            total
        ]
        worksheet.append(row_data)

    for cell in worksheet.iter_rows(min_row=2, min_col=3, max_col=3):
        for cell in cell:
            cell.number_format = "#,##0.00"
            
    # Customize column widths and alignment
    for column in worksheet.columns:
        max_length = 0
        column_name = column[0].column_letter
        for cell in column:
            try:
                value = cell.value
                cell.alignment = Alignment(wrap_text=True)
                if value is not None and len(str(value)) > max_length:
                    max_length = len(str(value))
            except:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column_name].width = adjusted_width
        for cell in column:
            cell.alignment = Alignment(wrapText=True)
    
    # Save the workbook to a BytesIO buffer
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    
    # Save the Excel file to disk
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sales_dir = os.path.join(root_dir, 'sales')
    os.makedirs(sales_dir, exist_ok=True)
    
    # Save the Excel file to the sales directory
    file_path = os.path.join(sales_dir, 'order_details.xlsx')
    with open(file_path, 'wb') as f:
        f.write(buffer.getvalue())
    
