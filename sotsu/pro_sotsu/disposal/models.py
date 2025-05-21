from django.db import models
from menu.models import Product
from django.contrib.auth import get_user_model
from django.utils.timezone import now  # デフォルト値に使用

User = get_user_model()

class Disposal(models.Model):
    disposal_menu = models.ForeignKey(Product, on_delete=models.CASCADE)  # 商品は ForeignKey で設定
    category = models.CharField(max_length=50, blank=True, null=True)
    price = models.PositiveIntegerField()
    disposal_quantity = models.PositiveIntegerField(default=1)
    disposal_date = models.DateField(default=now, blank=True, null=True)
    disposal_notes = models.TextField(blank=True, null=True, help_text="任意の情報を追加できます")
    disposal_registrant = models.CharField(max_length=100)
    store = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.disposal_menu} - {self.store.username}"

