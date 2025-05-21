# urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.food_list, name='food_list'),
    path('new/', views.food_form, name='food_form'),
    path('edit/<int:food_id>/', views.food_edit, name='food_edit'),
    path('delete/<int:food_id>/', views.food_delete, name='food_delete'),
    path('ingredient_confirm_delete/<int:food_id>/', views.ingredient_confirm_delete, name='ingredient_confirm_delete'),  # 確認ページのURL
    path('detail/<int:food_id>/', views.food_detail, name='food_detail'),
    path('main_page/', views.main_page, name='main_page'),
    
    
    path('logout_confirm/', views.logout_confirm, name='logout_confirm'),
    path('logout/', views.logout_view, name='logout'),
]

