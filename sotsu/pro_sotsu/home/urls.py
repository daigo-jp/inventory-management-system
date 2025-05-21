from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('signup/', views.register_store, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('main_page/', views.home, name='main_page'),
    path('register/success/', views.registration_success, name='registration_success'),  # 成功画面
]
