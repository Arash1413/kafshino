from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'city', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
            'phone': forms.TextInput(attrs={'placeholder': 'شماره موبایل'}),
            'city': forms.TextInput(attrs={'placeholder': 'شهر'}),
            'address': forms.Textarea(attrs={'placeholder': 'آدرس دقیق پستی', 'rows': 3}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'کد پستی'}),
        }