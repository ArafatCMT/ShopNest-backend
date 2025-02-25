from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from users.models import Customer, UsedToken
import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
# Create your views here.

class RegistrationView(APIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            # print(customer, customer.id)

            # token genarate kortaci
            token = jwt.encode(
                {
                    'user_id':user.id,
                    'email': user.email,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=15)  #  15 minute
                },
                settings.SECRET_KEY,
                algorithm="HS256"
            )

            verification_link = f"http://127.0.0.1:8000/verify/email/{token}"

            email_subject = 'Verify Your Account on ShopNest'
            email_body = render_to_string('verification_mail.html', {'verification_link': verification_link})
            email = EmailMultiAlternatives(email_subject, '' , to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            # print(user)
            return Response("Check your email for confirmation", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def Activate(token):
    try:
        # check kortaci token ta age used hoica ki na 
        if UsedToken.objects.filter(token=token).exists():
            return {'error': "Token already used!", 'status': status.HTTP_400_BAD_REQUEST}
        
        # token ta decode kortaci
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        # user ke get kore neye astici
        user = User.objects.get(id=payload['user_id']) 

        if not user.is_active:
            user.is_active = True
            user.save()

            # token ta store koratci karon token age used hoi nai 
            UsedToken.objects.create(token=token)
            return {'message': 'Email verified successfully!', 'status': status.HTTP_200_OK}
        return {"message": "Email already verified!", "status": status.HTTP_200_OK}
    
    except jwt.ExpiredSignatureError:
        return {"error": "Verification link expired!", "status": status.HTTP_400_BAD_REQUEST}
    except jwt.DecodeError:
        return {"error": "Invalid verification link!", "status": status.HTTP_400_BAD_REQUEST}
    except User.DoesNotExist:
        return {"error": "User not found!", "status": status.HTTP_404_NOT_FOUND}


class LoginView(APIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(username,password)

            user = authenticate(username=username, password=password)

            if user is not None:
                customer = Customer.objects.get(user = user)
                
                return Response(serializer.data, {'details': 'login successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "Invalid Credential"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)
