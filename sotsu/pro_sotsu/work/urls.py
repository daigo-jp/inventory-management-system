# work/urls.py
from django.urls import path
from . import views

urlpatterns = [
  path('work_start_check/', views.work_start_check, name='work_start_check'),  # ルーティングの設定
  path('work_start_ok/', views.work_start_ok, name='work_start_ok'),  # 営業終了完了
  path('work_end_check/', views.work_end_check, name='work_end_check'),  # 営業終了確認
  path('work_end_ok/', views.work_end_ok, name='work_end_ok'),  # 営業終了完了
]
