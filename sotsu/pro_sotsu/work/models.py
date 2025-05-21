# work/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings

class WorkDatetime(models.Model):
    store_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    work_start_time = models.DateTimeField(null=True, blank=True)
    work_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.store_name}の勤務時間"
