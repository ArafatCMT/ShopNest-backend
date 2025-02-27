from django.shortcuts import render
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class AddCategory(APIView):
    serializer_class = serializers.CategorySerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'details': 'category added successfully'} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors)