# order/forms.py
from django import forms
from menu.models import Product  # menu.modelsから参照

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price']
