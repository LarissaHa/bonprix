from django import forms

from .models import Review, Product

class ReviewForm(forms.ModelForm):

    class Meta:
         model = Review
         fields = ('text', 'stars')

class ReviewFormUnknown(forms.ModelForm):

    class Meta:
         model = Review
         fields = ('product_number', 'text', 'stars')
