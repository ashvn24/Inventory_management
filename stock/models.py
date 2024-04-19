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
    
    def __str__(self):
        return f'{self.Name}-{self.quantity}'
    
class ProductImages(Product):
    image = models.ImageField(upload_to='products/')
    
    