from django import forms
from .models import Product, ProductIngredient
from foods.models import Food
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Food.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # チェックボックスで表示
        required=True  # 必須に設定
    )

    class Meta:
        model = Product
        fields = ['name','category', 'price', 'notes', 'ingredients']

    def clean_ingredients(self):
        ingredients = self.cleaned_data.get('ingredients')
        if not ingredients:
            raise ValidationError("少なくとも1つの食材を選択してください。")
        return ingredients


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # ユーザーを取得
        super().__init__(*args, **kwargs)
        if self.user:
            # ログイン中のユーザーに関連付けられた食材のみを取得
            self.fields['ingredients'].queryset = Food.objects.filter(store=self.user)

def clean_name(self):
    name = self.cleaned_data.get('name')
    # デバッグ: インスタンスのPKを表示
    print(f"デバッグ: 現在のインスタンスPK - {self.instance.pk}")
    
    if Product.objects.filter(name=name, store=self.user).exclude(pk=self.instance.pk).exists():
        raise forms.ValidationError(f"商品名 '{name}' は既に登録されています。")
    return name

