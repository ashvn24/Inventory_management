from rest_framework import serializers
from .models import *


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model =  Category
        fields =  ['id', 'id_no', 'Name']
        

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'Name', 'product_id', 'price', 'quantity', 'category_name']
        
    def get_category_name(self, obj):
        return obj.category.Name
        
class ProductImage(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields ='__all__'
        