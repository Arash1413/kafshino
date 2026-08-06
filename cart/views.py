from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size') # دریافت سایز از فرم
    cart.add(product=product, size=size)
    return redirect('cart:cart_detail')

def cart_remove(request, product_id, size):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product.id, size)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})