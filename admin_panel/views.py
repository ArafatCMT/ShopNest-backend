from django.shortcuts import render
from rest_framework.views import APIView
from users import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Admin
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class AdminLoginView(APIView): 
    serializer_class = serializers.LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            print(user)
            if user and user.is_active and user.is_staff and user.is_superuser:
                try:
                    admin = Admin.objects.get(user=user)
                except Exception:
                    return Response({'error': "Invalid Credential"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if admin.is_admin:
                        print(admin)
                        login(request,user)
                        refresh = RefreshToken.for_user(user)

                        return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'admin_id' : admin.id
                        })
            else:
                return Response({'error': "Invalid Credential"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)


