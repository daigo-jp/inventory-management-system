from django import forms
from .models import StoreAccount

class StoreAccountForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="パスワード再入力"
    )

    class Meta:
        model = StoreAccount
        fields = [
            'store_name', 'postal_code', 'address', 'phone_number',
            'manager_name', 'manager_email', 'manager_phone', 'password', 'confirm_password'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "パスワードが一致しません。")

        return cleaned_data

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data["password"])
        if commit:
            account.save()
        return account

