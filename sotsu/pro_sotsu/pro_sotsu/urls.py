# プロジェクトルートの urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # ホーム画面のURL
    path('foods/', include('foods.urls')),  # foods アプリのURLを '/foods/' に割り当て
    path('menu/', include('menu.urls')), 
    path('disposal/',include('disposal.urls')),
    path('sales/', include('sales.urls')),
    path('work/', include('work.urls')),    
    path('order/', include('order.urls')),
]

