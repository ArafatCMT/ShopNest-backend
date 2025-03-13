from django.shortcuts import render
from rest_framework.views import APIView
from users import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Admin
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsNotAuthenticated
from rest_framework.permissions import IsAdminUser
from .serializers import AdminSerializer

class AdminLoginView(APIView): 
    permission_classes=[IsNotAuthenticated]
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
                        # print(admin)
                        login(request,user)
                        refresh_token = RefreshToken.for_user(user)

                        return Response({
                            'refresh_token': str(refresh_token),
                            'access_token': str(refresh_token.access_token),
                            'admin_id' : admin.id
                        })
            else:
                return Response({'error': "Invalid Credential"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)


class AdminProfileView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminSerializer

    def get(self, request):
        admin = Admin.objects.get(user=request.user)
        serializer = AdminSerializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        try:
            admin = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            return Response({"error":"You are not authorized to update this profile."})
        
        serializer = serializers.CustomerSerializer(admin, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)