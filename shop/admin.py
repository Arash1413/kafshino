from xml.etree.ElementTree import Comment

from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Size, Comment

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
    list_display = ['show_image', 'name', 'category', 'price', 'available', 'created', 'is_best_selling', 'is_new']
    
    # فیلترها در سمت راست
    list_filter = ['available', 'created', 'updated', 'category', 'is_new', 'is_best_selling']
    
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

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'active', 'created']
    list_filter = ['active', 'created', 'rating']
    search_fields = ['content', 'user__username']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "تایید نظرات انتخاب شده"