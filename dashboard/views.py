from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.decorators import login_required

from core.forms import BlogPostForm
from dashboard.models import Cart, CartItem
from item.models import Item
from .models import Post

@login_required
def index(request):
    items = Item.objects.filter(created_by=(request.user)).order_by('-created_at')
    
    return render( request, 'dashboard/index.html',{
        'items':items
    })
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('dashboard:cart')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.get_total_item_price() for item in cart_items)

    return render(request, 'dashboard/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, item=item).first()

    if cart_item:
        cart_item.delete()

    return redirect('dashboard:cart')


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('dashboard:profile')
    return render(request, 'core/profile.html')
# @login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'core/post_detail.html', {'post': post})
# views.py
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import MpesaPayment
import base64
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


# Function to get access token
def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_url, auth=(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    return mpesa_access_token['access_token']

# Function to initiate payment
def lipa_na_mpesa_online(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        amount = request.POST['amount']
        access_token = get_access_token()
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {'Authorization': 'Bearer %s' % access_token}
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode('utf-8')).decode('utf-8')

        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": "Test123",
            "TransactionDesc": "Payment for goods"
        }

        response = requests.post(api_url, json=payload, headers=headers)
        mpesa_response = json.loads(response.text)
        if mpesa_response.get('ResponseCode') == '0':
            MpesaPayment.objects.create(
                transaction_id=mpesa_response['CheckoutRequestID'],
                amount=amount,
                phone_number=phone_number,
                account_reference=payload['AccountReference'],
                transaction_description=payload['TransactionDesc'],
                status='Pending'
            )
            return JsonResponse({'success': True, 'message': 'Payment initiated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Payment initiation failed'})
    return render(request, 'dashboard/lipa_na_mpesa.html')

# Function to handle callback
@csrf_exempt 
def mpesa_callback(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment_data = json.loads(mpesa_body)
    result_code = mpesa_payment_data['Body']['stkCallback']['ResultCode']
    checkout_request_id = mpesa_payment_data['Body']['stkCallback']['CheckoutRequestID']

    mpesa_payment = MpesaPayment.objects.get(transaction_id=checkout_request_id)

    if result_code == 0:
        mpesa_payment.status = 'Completed'
    else:
        mpesa_payment.status = 'Failed'
    
    mpesa_payment.save()

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})



# Create your views here.
@login_required
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, 'Blog post added successfully.')
            return redirect('dashboard:post_list')
    else:
        form = BlogPostForm()
    return render(request, 'core/add_blog_post.html', {'form': form})
@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('dashboard:post_list')

    return render(request, 'core/post_delete.html', {'post': post})