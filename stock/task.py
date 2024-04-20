import random
from celery import shared_task
from django.conf import settings
from .models import Order, CartOrder, Shipment, Product
from django.core.mail import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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