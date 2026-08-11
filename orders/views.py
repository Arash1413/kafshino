import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm
from .models import Order, OrderItem
from cart.cart import Cart
from .utils import send_otp_sms
import requests # حتماً این کتابخانه را نصب داشته باشید: pip install requests
from django.conf import settings

# ۱. ویوی ثبت سفارش و ارسال پیامک
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'],
                    price=item['price'], quantity=item['quantity'], size=item['size']
                )
            
            # بخش OTP
            otp_code = random.randint(10000, 99999)
            request.session['otp_code'] = str(otp_code)
            request.session['otp_order_id'] = order.id
            
            send_otp_sms(order.phone, otp_code)
            return redirect('orders:otp_verify')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

# ۲. ویوی تایید کد پیامکی
def otp_verify(request):
    if request.method == 'POST':
        user_code = request.POST.get('otp_code')
        saved_code = request.session.get('otp_code')
        order_id = request.session.get('otp_order_id')
        
        if user_code == saved_code:
            del request.session['otp_code']
            cart = Cart(request)
            cart.clear()
            return render(request, 'orders/created.html', {'order_id': order_id})
        else:
            return render(request, 'orders/otp_verify.html', {'error': 'کد وارد شده صحیح نیست.'})
            
    return render(request, 'orders/otp_verify.html')

# ۳. ویوی لیست سفارشات کاربر (همان تابعی که جایش خالی بود)
@login_required
def user_orders(request):
    orders = request.user.orders.all()
    return render(request, 'orders/user_orders.html', {'orders': orders})