from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields =['email', 'password']
        extra_kwargs ={
            'password':{'write_only':True}
        }
    
    def create(self, validated_data):

        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email =serializers.EmailField()
    password= serializers.CharField(write_only=True)
    access_token= serializers.CharField(read_only=True) 
    refresh_token = serializers.CharField(read_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        request = self.context.get("request")
        
        user = authenticate(request, email=email, password=password)
        login(request,user)
        if not user:
            raise AuthenticationFailed('user not found')   
        
        token = user.get_token()     
        
        return{
            'email':user.email,
            'access_token': str(token.get('access')),
            'refresh_token': str(token.get('refresh'))
        }
        
class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'