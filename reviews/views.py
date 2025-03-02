from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from . import serializers
from users import models
from products import models
from orders import models
from .models import Review
# Create your views here.
class AddReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = serializers.ReviewSerializer(data = request.data)
        customer = models.Customer.objects.get(user=request.user)
        print(customer)
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product']
            product = models.Product.objects.get(pk=product_id)
            print(product)

            order = models.Order.objects.filter(product=product, customer=customer, order_status='Delivered')
            print(order)

            if not order: # order list empty hole , mne product purchase kore nai
                return response.Response({'error':"You can only review a product that you have purchased. Please purchase the product first."}, status=status.HTTP_400_BAD_REQUEST)

            comment = serializer.validated_data['comment']
            rating = serializer.validated_data['rating']

            Review.objects.create(customer=customer, product=product, comment=comment, rating=rating)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


