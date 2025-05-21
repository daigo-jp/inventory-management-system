from django.db import models
from django.contrib.auth import get_user_model
from foods.models import Food

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField()
    ingredients = models.ManyToManyField('foods.Food', through='ProductIngredient')
    store = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # デフォルトのユーザーIDを指定
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, help_text="任意の情報を追加できます")

    def __str__(self):
        return self.name
    
    def get_stock(self):
        stock = None
        for ingredient in self.productingredient_set.all():
            # 各食材に対して、使用可能な最大量を計算
            max_producible = ingredient.food.quantity // ingredient.quantity
            # 最小値を在庫とする
            if stock is None or max_producible < stock:
                stock = max_producible
        return stock if stock is not None else 0  # 在庫が0または計算不可の場合は0を返す

class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    food = models.ForeignKey('foods.Food', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.food.name} ({self.quantity})"