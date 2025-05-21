# sales/forms.py

from django import forms
from .models import Sales  # 売上モデル
from menu.models import Product  # 商品モデル

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['product', 'quantity']  # priceフィールドを削除
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # ログイン中のユーザーに関連付けられた商品のみを取得
            self.fields['product'].queryset = Product.objects.filter(store=user)
