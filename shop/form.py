# shop/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-4 bg-gray-50 border-2 border-gray-100 rounded-[1.5rem] outline-none focus:border-[#428e91] transition',
                'placeholder': 'تجربه خرید خود را بنویسید...',
                'rows': 4
            }),
            'rating': forms.Select(choices=[(i, f'{i} ستاره') for i in range(1, 6)], attrs={
                'class': 'bg-gray-50 border-none rounded-xl p-2 outline-none'
            })
        }