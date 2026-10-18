from django.db import models
from django.urls import reverse  # ۱. این را اضافه کن
from django.contrib.auth.models import User

class Size(models.Model):
    name = models.CharField(max_length=10, verbose_name="سایز")

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام دسته بندی")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی‌ها"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام برند")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"

    def __str__(self):
        return self.name

class Product(models.Model):
    sizes = models.ManyToManyField(Size, related_name='products', verbose_name="سایزهای موجود")
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name="تصویر اصلی")
    description = models.TextField(verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت (تومان)")
    available = models.BooleanField(default=True, verbose_name="موجود")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_new = models.BooleanField(default=False, verbose_name="نمایش در جدیدترین‌ها")
    is_best_selling = models.BooleanField(default=False, verbose_name="نمایش در پرفروش‌ها")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', null=True, blank=True, verbose_name="برند")

    def get_absolute_url(self):
    # حتماً کلمه shop: را قبل از نام آدرس بگذارید
        return reverse('shop:product_detail', args=[self.id, self.slug])

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name



class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/%Y/%m/%d/')

    class Meta:
        verbose_name = "تصویر گالری"
        verbose_name_plural = "گالری تصاویر"



# در فایل shop/models.py



# حالا مدل Product را ویرایش کنید و فیلد برند را به آن اضافه کنید:
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name="محصول")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="کاربر")
    content = models.TextField(verbose_name="متن نظر")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="امتیاز") # ۱ تا ۵
    active = models.BooleanField(default=True, verbose_name="وضعیت انتشار") # برای تایید توسط مدیر
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f'نظر {self.user.first_name} برای {self.product.name}'