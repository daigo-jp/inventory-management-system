# sales/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_list, name='sales_list'),  # 売上一覧のURL
    path('create/', views.sales_create, name='sales_create'),  # 売上登録ページ
    path('get_stock/<int:product_id>/', views.get_stock, name='get_stock'),  # 在庫数取得API
    path('sales/graph/', views.sales_graph, name='sales_graph'),
]
