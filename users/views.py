from django.shortcuts import render
from .models import CustomUser
from .serializers import *
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# Create your views here.

class UserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializers
    
    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)
        
        return Response(response.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListUser(generics.ListAPIView):
    serializer_class = ListSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    # authentication_classes =[SessionAuthentication]
    
    
    