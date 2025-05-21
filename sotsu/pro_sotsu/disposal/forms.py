from django.core.exceptions import ValidationError
from django import forms
from .models import Disposal
from menu.models import Product  # 必要な場合にインポート

class DisposalForm(forms.ModelForm):
    product = forms.ModelMultipleChoiceField(
        queryset=Product.objects.none(),  # 初期状態では空にしておく
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Disposal
        fields = ['disposal_menu', 'disposal_date', 'category', 'price', 'disposal_quantity', 'disposal_notes', 'disposal_registrant', 'product']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 'user' を受け取る
        super().__init__(*args, **kwargs)
        
        if user:
            # ユーザーの店舗に絞った商品を 'disposal_menu' と 'product' に設定
            self.fields['disposal_menu'].queryset = Product.objects.filter(store=user)
            self.fields['product'].queryset = Product.objects.filter(store=user)

    def clean(self):
        cleaned_data = super().clean()

        # disposal_menu からカテゴリと価格を取得
        product = cleaned_data.get('disposal_menu')
        if product:
            # 'disposal_menu' が有効な Product オブジェクトであるか確認
            if isinstance(product, Product):
                cleaned_data['category'] = product.category
                cleaned_data['price'] = product.price
            else:
                self.add_error('disposal_menu', '選択された商品が無効です。')

        return cleaned_data