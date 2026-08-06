from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # گرفتن ۳ تا از جدیدترین محصولات
    latest_products = Product.objects.filter(available=True).order_by('-created')[:3]
    
    # فعلاً به عنوان نمونه ۳ تا محصول دیگر برای پرفروش‌ها
    best_selling = Product.objects.filter(available=True).order_by('?')[:3]

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'latest_products': latest_products,
        'best_selling': best_selling
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # پیدا کردن محصولات مرتبط (همان دسته بندی)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'related_products': related_products
    })