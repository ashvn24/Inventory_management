from django.db import models

# Create your models here.

class Category(models.Model):
    Name = models.CharField(max_length=50)
    id_no = models.IntegerField()
    
    def __str__(self):
        return self.Name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    product_id = models.IntegerField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    images = models.ImageField(upload_to='product/')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.Name}-{self.quantity}'
    
    
    
class Order(models.Model):
    order_id = models.IntegerField()
    Name = models.CharField(max_length=200)
    email =models.EmailField()
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    Address = models.TextField()
    
    def __str__(self):
        return self.Name
    
    
class CartOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity =  models.IntegerField(null=True, blank=True)    
    
    def __str__(self):
        return f'Order:{self.order.Name} , Quantity: {self.quantity}'
    
class Shipment(models.Model):
    ship_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False) 
    tracking_number = models.CharField(max_length=50, null=True)
    date_shipped = models.DateTimeField(auto_now_add=True)
    items = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    address = models.TextField()
    
    def __str__(self):
        return self.ship_order.Name
    
class Order_history(models.Model):
    prev_order = models.ForeignKey(Order, on_delete= models.CASCADE)
    order_cart = models.ForeignKey(CartOrder, on_delete= models.CASCADE)
    
    def __str__(self):
        return  "Previous Order : "+self.prev_order.Name
    