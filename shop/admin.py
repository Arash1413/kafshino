from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Size

# برای اینکه بتوانیم در صفحه محصول، عکس‌های گالری را همزمان اضافه کنیم
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']
 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # پر شدن خودکار اسلاگ وقتی نام را تایپ می‌کنید

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # ستون‌هایی که در لیست محصولات نمایش داده می‌شوند
    list_display = ['show_image', 'name', 'category', 'price', 'available', 'created']
    
    # فیلترها در سمت راست
    list_filter = ['available', 'created', 'updated', 'category']
    
    # فیلدهایی که مستقیماً در لیست قابل ویرایش هستند (بسیار کاربردی)
    list_editable = ['price', 'available']
    
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    # متد نمایش پیش‌نمایش عکس در لیست
    def show_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="border-radius:10px;" />')
        return "بدون تصویر"
    show_image.short_description = "تصویر"