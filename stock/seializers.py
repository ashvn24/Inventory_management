from rest_framework import serializers
from .models import *
import random


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model =  Category
        fields =  ['id', 'id_no', 'Name']
        

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'Name', 'product_id', 'price', 'quantity','category', 'category_name','images']
        extra_kwargs ={
            'images':{'required':False},
            'category':{'write_only':True}
        }
        
    def get_category_name(self, obj):
        return obj.category.Name
    
class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'Name', 'Product', 'product_name', 'quantity', 'date']
        extra_kwargs ={
            'product':{'write_only':True},
            'order_id':{'read_only':True}
        }
        
    def get_product_name(self, obj):
        return obj.Product.Name
    
    def create(self, validated_data):
        validated_data['order_id'] = random.randint(100000,999999)
        return super().create(validated_data)
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrder
        fields ='__all__'
        
        
        
