from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
# from rest_framework.response import Response

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'error': "Password Dosn't Match"})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "email already exists"})
        
        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        # print(user, user.id)
        customer = models.Customer.objects.create(user=user)
        # print(customer.id)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)