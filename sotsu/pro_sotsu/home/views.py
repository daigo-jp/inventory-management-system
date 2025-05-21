# home/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import StoreAccountForm
from .models import StoreAccount

from django.utils import timezone

def register_store(request):
    if request.method == 'POST':
        form = StoreAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
        else:
            print("Form errors:", form.errors)  # デバッグ用
    else:
        form = StoreAccountForm()

    return render(request, 'home/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        password = request.POST.get('password')
        user = authenticate(request, username=store_name, password=password)
        if user is not None:
            # ユーザーが認証されたらログイン時刻を設定
            user.last_login = timezone.localtime(timezone.now())  # 現地時間に変換して保存
            user.save()  # 保存して更新
            login(request, user)
            return redirect('home')  # ログイン後のリダイレクト先
        else:
            error_message = "正しいユーザー名とパスワードを入力してください。"
            return render(request, 'home/login.html', {'error_message': error_message})
    return render(request, 'home/login.html')

def registration_success(request):
    return render(request, 'home/success.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home/home.html')
