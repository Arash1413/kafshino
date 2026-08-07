from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.db.models import Q  # این را حتماً اضافه کنید

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # منطق جستجو
    query = request.GET.get('query')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )

    # گرفتن ۳ تا از جدیدترین محصولات (برای نمایش در سایدبار یا بخش‌های دیگر)
    latest_products = Product.objects.filter(available=True).order_by('-created')[:3]
    best_selling = Product.objects.filter(available=True).order_by('?')[:3]

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'latest_products': latest_products,
        'best_selling': best_selling,
        'query': query # ارسال متن جستجو به تمپلیت
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # پیدا کردن محصولات مرتبط (همان دسته بندی)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'related_products': related_products
    })