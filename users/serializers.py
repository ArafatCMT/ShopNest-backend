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
    username = serializers.CharField(required = True, write_only=True)
    password = serializers.CharField(required = True, write_only=True)

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        read_only_fields = ['username']

class CustomerSerializer(serializers.ModelSerializer):
    # UserSerializer er field gula use korar jonno UserSerializer include korlam
    user = UserSerializer()

    class Meta:
        model = models.Customer
        fields = ['user', 'profile_picture_url', 'address', 'phone_number', 'gender', 'join_dated']

    def update(self, instance, validated_data):
        # pop method ta deye validated_data theke user field ke remove korlam. jehetu user ek ta nasted object.Jokhon user data thake na, tokhon None return korbe, ar error raise korbe na.
        user_data = validated_data.pop('user', None)
        # print(user_data)

        # User instance update hobe jodi user_data provide kora hoi.
        if user_data:
            user = instance.user
            # print(user)
            for key, value in user_data.items():
                # print(key,value)
                setattr(user, key, value) #update user serializer er fields
            user.save()

        # customer model er field gula update kora hocca
        for key,value in validated_data.items():
            setattr(instance, key, value) # update customer serializer er fields
            # print(key,value)
        instance.save()
        return instance