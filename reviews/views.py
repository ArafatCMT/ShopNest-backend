from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from . import serializers
from users import models
from products import models
from orders import models
from .models import Review
from rest_framework.exceptions import NotFound


# Create your views here.
class AddReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = serializers.ReviewSerializer(data = request.data)
        customer = models.Customer.objects.get(user=request.user)
        # print(customer)
        
        if serializer.is_valid():
            product = serializer.validated_data['product']

            order = models.Order.objects.filter(product=product, customer=customer, order_status='Delivered')
            # print(order)

            if not order: # order list empty hole , mne product purchase kore nai
                return response.Response({'error':"You can only review a product that you have purchased. Please purchase the product first."}, status=status.HTTP_400_BAD_REQUEST)

            comment = serializer.validated_data['comment']
            rating = serializer.validated_data['rating']

            # print(product.id,comment, rating)

            Review.objects.create(customer=customer, product=product, comment=comment, rating=rating)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise NotFound(detail="Review doesn't exist")
        
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = serializers.ReviewSerializer(review)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        review = self.get_object(pk)

        if review.customer.user != request.user:
            return response.Response({"error": "You are not authorized to update this review."}, status=status.HTTP_403_FORBIDDEN)
        # print('review',review)
        # je fields gula update kora jabe ta allowed_fields er moddhe bola holo
        allowed_fields = ['comment', 'rating']

        update_data = {key:value for key,value in request.data.items() if key in allowed_fields}
        # print('update',update_data)

        # check kortaci allowed_fields er value cara onno kono value ase ki na , shudu allowed_fields er value gula i nebe onno thai ek ta {} dictonary update_data te assign hobe
        if not update_data:
            return response.Response({"error": "No valid fields provided for update."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.ReviewSerializer(review, data=update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        review = self.get_object(pk)

        if review.customer.user != request.user:
            return response.Response({"error": "You are not authorized to delete this review."}, status=status.HTTP_403_FORBIDDEN)
        
        review.delete()
        return response.Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


