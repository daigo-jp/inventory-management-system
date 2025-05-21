# order/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),  # ここで確認
    path('product_list/', views.product_list, name='product_list'),  # 追加
    path('order_complete/', views.order_complete, name='order_complete'),  # 注文完了画面
    path('order/', views.order, name='order'),  # 追加
]