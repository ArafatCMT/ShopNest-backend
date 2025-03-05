from django.shortcuts import render
from . import models
from products.models import Product
from . import serializers
from users.models import Customer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
# Create your views here.

class AddToCartView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound({"detail":"product dosn't exist"})

    def post(self, request, pk):
        # print(request.user)
        product = self.get_object(pk)
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"error":"Customer dosn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        # filter kortaci cart e product ta already add kora ase  ki nai
        is_exist = models.Cart.objects.filter(product=product, customer=customer).exists()
        # jodi cart e product ta already add kora thake tobe shudu quantity ta 1 increase kore dicci 
        if is_exist:
            cart_item = models.Cart.objects.get(product=product, customer=customer)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.total_price = cart_item.quantity * cart_item.total_price
            cart_item.save()

            return Response({
                "message": "Cart item updated successfully.",
                "cart_item": serializers.CartSerializer(cart_item).data
            }, status=status.HTTP_200_OK)

        # cart e add na thakle abr notun object create hobe
        data = {
            "product": product.id,
            "customer": customer.id,
            "total_price": product.price
            }
        # print(data)
        serializer = serializers.CartSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerCartDetailView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"error":"Customer doesn't exist"})
        
        cart_list = models.Cart.objects.filter(customer=customer)
        print(cart_list)
        serializer = self.serializer_class(cart_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)