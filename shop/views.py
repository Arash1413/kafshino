from django.shortcuts import render, get_object_or_404
from .models import Brand, Category, Product
from django.db.models import Q  # این را حتماً اضافه کنید
from django.contrib import messages
from .form import CommentForm
from django.shortcuts import redirect


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
    latest_products = Product.objects.filter(available=True, is_new=True)[:4]
    best_selling = Product.objects.filter(available=True, is_best_selling=True)[:4]

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

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    brands = Brand.objects.all() # دریافت همه برندها برای نمایش در سایدبار
    products = Product.objects.filter(available=True)

    # ۱. فیلتر جستجو (که قبلاً داشتیم)
    query = request.GET.get('query')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # ۲. فیلتر بر اساس دسته بندی
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # ۳. فیلتر بر اساس برند
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    # ۴. فیلتر بر اساس قیمت
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # ۵. مرتب سازی (جدیدترین، ارزان‌ترین، گران‌ترین)
    sort = request.GET.get('sort')
    if sort == 'cheap':
        products = products.order_by('price')
    elif sort == 'expensive':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created')

    latest_products = Product.objects.filter(available=True).order_by('-created')[:3]
    best_selling = Product.objects.filter(available=True).order_by('?')[:3]

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'brands': brands,
        'products': products,
        'latest_products': latest_products,
        'best_selling': best_selling,
        'query': query
    })


def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "برای ثبت نظر ابتدا باید وارد حساب خود شوید.")
            return redirect('account:login')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            messages.success(request, "نظر شما با موفقیت ثبت شد.")
    
    return redirect(product.get_absolute_url())


def about_us(request):
    return render(request, 'shop/about.html')