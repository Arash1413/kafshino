from decimal import Decimal
from django.conf import settings
from shop.models import Product
from django.contrib import messages  # این درست است

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, size=None, override_quantity=False):
        product_id = str(product.id)
        # ترکیب آی‌دی و سایز برای اینکه اگر از یک کفش دو سایز مختلف خواست، جدا ذخیره شود
        item_key = f"{product_id}_{size}" if size else product_id
        
        if item_key not in self.cart:
            self.cart[item_key] = {
                'quantity': 0,
                'price': str(product.price),
                'size': size
            }
        
        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product_id, size=None):
        item_key = f"{product_id}_{size}" if size else str(product_id)
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def __iter__(self):
        item_keys = self.cart.keys()
        product_ids = [k.split('_')[0] for k in item_keys]
        products = Product.objects.filter(id__in=product_ids)
        
        # ساخت یک کپی برای جلوگیری از تغییر داده‌های اصلی سشن
        cart = {k: v.copy() for k, v in self.cart.items()}
        
        for product in products:
            for key in cart.keys():
                if key.startswith(str(product.id)):
                    cart[key]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


    # در انتهای کلاس Cart در فایل cart/cart.py
    def __len__(self):
        """
        محاسبه تعداد کل آیتم‌های موجود در سبد خرید
        """
        return sum(item['quantity'] for item in self.cart.values())