from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
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
from rest_framework_simplejwt.tokens import RefreshToken
from admin_panel.permissions import IsNotAuthenticated
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def token_genarate(user):
    token = jwt.encode(
            {
                'user_id':user.id,
                'email': user.email,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15)  #  15 minute
            },
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    return token

def SendEmail(user, verification_link):
    email_subject = 'Verify Your Account on ShopNest'
    email_body = render_to_string('verification_mail.html', {'verification_link': verification_link, 'username':user.username})
    email = EmailMultiAlternatives(
            subject=email_subject,
            body="",
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
    email.attach_alternative(email_body, "text/html")
    email.send()


class RegistrationView(APIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = serializers.RegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            # print(customer, customer.id)

            # token genarate kortaci
            token = token_genarate(user)

            verification_link = f"http://127.0.0.1:8000/api/verify/email/{token}"
            
            # SendEmail function all 
            SendEmail(user, verification_link)

            # print(user)
            return Response("Check your email for confirmation", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def Activate(request, token):
    try:
        # check kortaci token ta age used hoica ki na
        if UsedToken.objects.filter(token=token).exists():
            return render(request, 'error.html', {'error': "Token already used!"})
        
        # token ta decode kortaci
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        # user ke get kore neye astici
        user = User.objects.get(id=payload['user_id']) 

        if not user.is_active:
            print(user.username)
            user.is_active = True
            user.save()

            # token ta store koratci karon token age used hoi nai 
            UsedToken.objects.create(token=token)
            return redirect('login')
        return redirect('register')
    
    except jwt.ExpiredSignatureError:
        return render(request, 'error.html', {'error': "Verification link expired!"})
    except jwt.DecodeError:
        return render(request, 'error.html', {'error': "Invalid verification link!"})
    except User.DoesNotExist:
        return render(request, 'error.html', {'error': "User not found!"})


class LoginView(APIView):
    permission_classes=[IsNotAuthenticated]
    serializer_class = serializers.LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(username,password)

            user = authenticate(username=username, password=password)
            print(user)

            if user:
                try:            
                    customer = Customer.objects.get(user = user)
                except Customer.DoesNotExist:
                    return Response({'error': "Invalid Credential"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    login(request, user)
                    refresh_token = RefreshToken.for_user(user)
                
                    return Response({
                        'refresh_token' : str(refresh_token),
                        'access_token': str(refresh_token.access_token),
                        'customer_id': customer.id
                    }, status.HTTP_200_OK)
            else:
                return Response({'error': "Invalid Credential"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LogoutSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh_token']
            # print(refresh_token)
            try: 
                token = RefreshToken(refresh_token)
                # print('logout')
                token.blacklist()
                return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
            except Exception:
                return Response({'error':"Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):

    def post(self, request):
        refresh_token = request.data.get("refresh")  #  Key must match frontend
        # print(f"refresh_token:- {refresh_token}")

        if not refresh_token:
            return Response({"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # print('Before RefreshToken')
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)  #  Access token generate korchi
            # print('After RefreshToken')
            return Response({
                "access_token": new_access_token, #  Only access token return korchi
            }, status=status.HTTP_200_OK)
        
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        serializer = serializers.ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not request.user.check_password(raw_password=password):
                return Response({'error': 'password not match'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                request.user.set_password(new_password)
                request.user.save()
                # print(password, new_password)
                # print(request.user)
                return Response({'success': 'password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, fromat=None):
        customer = Customer.objects.get(user=request.user)
        serializer = serializers.CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"error":"Customer dosn't exist."})
        else:
            serializer = serializers.CustomerSerializer(customer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





