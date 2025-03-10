from django.shortcuts import render
from sslcommerz_lib import SSLCOMMERZ
from users.models import Customer
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from orders.models import Order
# Create your views here.

import uuid
import random
import hashlib

def generate_transaction_id():
    # Generate a UUID (Universally Unique Identifier)
    unique_id = uuid.uuid4()
    
    # Convert UUID to a hash-based 12-digit number
    hashed_id = int(hashlib.sha256(str(unique_id).encode()).hexdigest(), 16)
    
    # Ensure it's within 12-digit range
    transaction_id = str(hashed_id)[0:12]
    
    return transaction_id

@csrf_exempt  # CSRF check bypass করা হলো
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Payment(request):
    try:
        customer = Customer.objects.get(user=request.user)
        print(customer)
    except Customer.DoesNotExist:
        return Response({"detail":"user doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
    
    order_list = Order.objects.filter(customer=customer, order_status='Pending')
    total_amount = 0
    if not order_list.exists():
        return Response(
    {"detail": "You have not placed any order yet. Please add products to your cart and complete checkout before proceeding to payment."},
    status=status.HTTP_400_BAD_REQUEST)

    # loop caliye order item gular status r payment status update kora hocca
    for orderItem in order_list:
        total_amount += orderItem.total_amount
        product = Product.objects.get(pk=orderItem.product.id)
        print(product)

    settings = { 
        'store_id': 'shopn67ce83cc857d4',
        'store_pass': 'shopn67ce83cc857d4@ssl',
        'issandbox': True 
    }

    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = total_amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = generate_transaction_id()
    post_body['success_url'] = "http://127.0.0.1:8000/api/login/"
    post_body['fail_url'] = "http://127.0.0.1:8000/api/register/"
    post_body['cancel_url'] = "your cancel url"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{customer.user.first_name} {customer.user.last_name}"
    post_body['cus_email'] = f"{customer.user.email}"
    post_body['cus_phone'] = f"{customer.phone_number}"
    post_body['cus_add1'] = f"{customer.address}"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) 

    if 'GatewayPageURL' in response:
        return Response({"payment_url": response['GatewayPageURL']}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Payment session creation failed.", "response": response}, status=status.HTTP_400_BAD_REQUEST)