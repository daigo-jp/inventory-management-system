from django.urls import path
from . import views

urlpatterns = [
    path('disposal/manage/', views.disposal_manage, name='disposal_manage'),
    path('register/', views.disposal_register, name='disposal_register'),
    path('edit/<int:disposal_id>/', views.disposal_edit, name='disposal_edit'), 
    path('delete/<int:disposal_id>/', views.disposal_delete, name='disposal_delete'),  
    path('detail/<int:disposal_id>/', views.disposal_detail, name='disposal_detail'),    
 
]
