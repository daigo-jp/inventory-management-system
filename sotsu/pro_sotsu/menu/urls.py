from django.urls import path
from . import views

urlpatterns = [
    path('menu/list/', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),  # 編集用のURLパターン
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),  # 削除用のURLパターン
    path('<int:pk>/detail/', views.product_detail, name='product_detail'),  # 詳細用のURLパターン
]
