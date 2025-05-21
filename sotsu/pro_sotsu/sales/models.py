# sales/models.py

from django.db import models
from datetime import datetime
from menu.models import Product  # menuアプリのProductモデルをインポート

class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 商品モデルへの外部キー
    quantity = models.PositiveIntegerField()  # 販売した数量
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 1単位あたりの販売価格
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # 合計金額
    sale_date = models.DateTimeField(default=datetime.now)  # 販売日時

    def save(self, *args, **kwargs):
        # 合計金額を計算（販売数量 * 単価）
        self.total_cost = self.quantity * self.price
        super(Sales, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units sold"
