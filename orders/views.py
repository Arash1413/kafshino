import random
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse # این مورد در کد شما کم بود و باعث خطا می‌شد

from .forms import OrderCreateForm
from .models import Order, OrderItem
from cart.cart import Cart
from .utils import send_otp_sms

# ۱. ویوی ثبت سفارش و ارسال پیامک
def order_create(request):
    cart = Cart(request)
    # اگر سبد خرید خالی بود، اجازه دسترسی به این صفحه را نده
    if len(cart) == 0:
        return redirect('cart:cart_detail')

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

# ۲. ویوی تایید کد پیامکی و انتقال به درگاه
def otp_verify(request):
    error = None
    if request.method == 'POST':
        user_code = request.POST.get('otp_code')
        saved_code = request.session.get('otp_code')
        order_id = request.session.get('otp_order_id')
        
        if user_code == saved_code:
            order = get_object_or_404(Order, id=order_id)
            cart = Cart(request)
            amount = int(cart.get_total_price())

            # پارامترهای ارسالی به آقای پرداخت
            data = {
                'pin': settings.AQAYEPARDAKHT_PIN,
                'amount': amount,
                'callback': request.build_absolute_uri(reverse('orders:payment_callback')),
                'mobile': order.phone,
                'invoice_id': order.id,
            }

            try:
                response = requests.post('https://panel.aqayepardakht.ir/api/v2/create', data=data)
                result = response.json()

                print("--- Gateway Response ---")
                print(result) 
                print("------------------------")

                if result['status'] == 'success':
                    # ذخیره transid در مدل سفارش
                    order.tracking_code = result['transid']
                    order.save()
                    # حذف کد OTP از سشن برای امنیت
                    del request.session['otp_code']
                    return redirect(f"https://panel.aqayepardakht.ir/startpay/{result['transid']}")
                else:
                    error = f"خطا در اتصال به درگاه: {result.get('code', 'نامشخص')}"
            except:
                error = "خطای غیرمنتظره در اتصال به درگاه پرداخت."
        else:
            error = 'کد وارد شده صحیح نیست.'
            
    return render(request, 'orders/otp_verify.html', {'error': error})

# ۳. ویوی لیست سفارشات کاربر
@login_required
def user_orders(request):
    orders = request.user.orders.all()
    return render(request, 'orders/user_orders.html', {'orders': orders})

# ۴. ویوی بازگشت از درگاه پرداخت
def payment_callback(request):
    # آقای پرداخت معمولاً اطلاعات را به صورت POST یا GET می‌فرستد. 
    # برای اطمینان ما هر دو را چک می‌کنیم.
    transid = request.POST.get('transid') or request.GET.get('transid')
    status = request.POST.get('status') or request.GET.get('status')
    
    if not transid:
        return render(request, 'orders/payment_failed.html', {'error': 'تراکنشی یافت نشد.'})

    order = get_object_or_404(Order, tracking_code=transid)
    amount = int(order.get_total_cost())

    if status == '1': # پرداخت اولیه موفق
        data = {
            'pin': settings.AQAYEPARDAKHT_PIN,
            'amount': amount,
            'transid': transid
        }
        
        try:
            response = requests.post('https://panel.aqayepardakht.ir/api/v2/verify', data=data)
            verify_result = response.json()
            
            if verify_result['status'] == 'success':
                order.paid = True
                order.save()
                cart = Cart(request)
                cart.clear() # خالی کردن سبد فقط بعد از تایید نهایی پرداخت
                return render(request, 'orders/created.html', {'order': order})
            else:
                return render(request, 'orders/payment_failed.html', {'error': 'تایید پرداخت توسط بانک رد شد.'})
        except:
             return render(request, 'orders/payment_failed.html', {'error': 'خطای فنی در تایید تراکنش.'})
    else:
        return render(request, 'orders/payment_failed.html', {'error': 'پرداخت لغو شد یا با خطا مواجه شد.'})