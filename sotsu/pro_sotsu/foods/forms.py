from django import forms
from .models import Food

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        store = self.instance.store  # 編集対象の店舗
        if self.instance and self.instance.name == name:
            return name
        # 同じ店舗内で同じ食品名がすでに登録されているか確認
        if Food.objects.filter(name=name, store=store).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(f"食品名 '{name}' は既に登録されています。")
        return name
