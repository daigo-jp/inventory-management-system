from django.db import models
from home.models import StoreAccount  # StoreAccountモデルをインポート

class Food(models.Model):
    store = models.ForeignKey(StoreAccount, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    cost = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    delivery_days = models.IntegerField(default=1)
    expiration_date = models.DateField()
    description = models.TextField(blank=True, null=True)  # 説明フィールド

    def __str__(self):
        return self.name
    
class WorkDatetime(models.Model):
    store_name = models.CharField(max_length=100)
    work_start_time = models.DateTimeField(null=True, blank=True)
    work_end_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.store_name