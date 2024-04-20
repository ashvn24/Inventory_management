from django.shortcuts import render
from rest_framework import generics, status

from stock.task import Check_cart, send_mail
from .models import *
from .seializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# Create your views here.

class CreateCategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]
    
class ManageCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
class ProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[ IsAuthenticated ]
    
class ProductManageAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class OrderCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = serializer.validated_data['Product']
        quantity = serializer.validated_data['quantity']
        
        if product.quantity < quantity:
            return Response({"error": "Insufficient quantity for the product"}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
            
class ManageCartAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartOrder
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.instance
        new_quantity =  instance.product.quantity
        print(new_quantity)
        # Check if the new quantity is not zero
        if new_quantity != 0:
            instance = serializer.save()
            Check_cart.delay(instance.id)
            return super().perform_update(serializer)
        else:
            send_mail.delay(instance.product.Name)
            raise serializers.ValidationError("product out of stock!")
        
