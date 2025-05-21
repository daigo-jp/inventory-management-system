from django.shortcuts import render, get_object_or_404, redirect
from .models import Food
from .forms import FoodForm
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from menu.models import Product
from django.contrib import messages
from django.db.models import Q 


# 食材一覧
@login_required
def food_list(request):
    store = request.user 
    query = request.GET.get('q') 

    if query:
        # 食材名または種類でフィルタリング
        foods = Food.objects.filter(
            store=store
        ).filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )
    else:
        # 全ての食材を取得
        foods = Food.objects.filter(store=store)

    # 有効期限を日本語形式にフォーマット
    for food in foods:
        food.expiration_date_jp = food.expiration_date.strftime('%Y年%m月%d日')

    # 営業状態をセッションから取得
    current_date = date.today().strftime('%Y年%m月%d日')  # 現在の日付を取得
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')

    # テンプレートへのデータ渡し
    return render(request, 'foods/food_list.html', {
        'foods': foods,
        'query': query,
        'current_date':current_date,
        'work_status': work_status,
        'store_name': store_names
    })

#食材登録
@login_required
def food_form(request):
    current_date = date.today().strftime('%Y年%m月%d日')  
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')

    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food_name = form.cleaned_data.get('name')
            store = request.user

            # 既存の削除済みデータがあるかチェック
            existing_food = Food.objects.filter(name__iexact=food_name, store=store).first()

            if existing_food:
                if existing_food.is_deleted:
                    # もし削除フラグがTrueなら復活させる
                    existing_food.is_deleted = False
                    existing_food.save()
                    messages.success(request, f"食品 '{food_name}' が復活しました。")
                    return redirect('food_list')
                else:
                    # すでに存在する場合はエラー
                    messages.error(request, f"食品名 '{food_name}' は既に登録されています。")
                    form.add_error('name', f"食品名 '{food_name}' は既に登録されています。")
            else:
                # 新規登録
                food = form.save(commit=False)
                food.store = store
                food.save()
                messages.success(request, f"食品 '{food_name}' が登録されました。")
                return redirect('food_list')
    else:
        form = FoodForm()

    return render(request, 'foods/food_form.html', {
        'current_date': current_date,
        'work_status': work_status,
        'store_name': store_names,
        'form': form
    })


# 食材編集
@login_required
def food_edit(request, food_id):
    store = request.user
    food = get_object_or_404(Food, id=food_id, store=store)
    current_date = date.today().strftime('%Y年%m月%d日') 
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            food = form.save(commit=False)
            food.store = store
            food.save()
            return redirect('food_list')
    else:
        form = FoodForm(instance=food)
    return render(request, 'foods/food_edit.html', {
        'current_date': current_date,
        'work_status':work_status,
        'store_name':store_names,
        'form': form,
        'food': food})

#食材削除
@login_required
def food_delete(request, food_id):
    store = request.user
    food = get_object_or_404(Food, id=food_id, store=store)
    associated_products = Product.objects.filter(ingredients=food)
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    # デバッグ用メッセージ
    print("food_deleteビューに入りました。")
    print("リクエストメソッド:", request.method)
    print("関連商品が存在するか:", associated_products.exists())

    if associated_products.exists():
        if request.method == 'POST' and 'confirm_delete' in request.POST:
            print("削除確認ボタンが押されました。関連商品と共に削除します。")
            associated_products.delete()
            food.delete()
            messages.success(request, "選択した食材と関連する商品が削除されました。")
            return redirect('food_list')
        
        print("関連商品が存在するため、削除確認画面を表示します。")
        return render(request, 'foods/ingredient_confirm_delete.html', {
            'current_date': current_date,
            'work_status':work_status,
            'store_name':store_names,
            'food': food,
            'associated_products': associated_products
        })

    if request.method == 'POST':
        print("関連する商品がなく、削除を実行します。")
        food.delete()
        messages.success(request, "選択した食材が削除されました。")
        return redirect('food_list')

    print("削除ページを表示します。")
    return render(request, 'foods/food_delete.html', {
        'current_date': current_date,
        'work_status':work_status,
        'store_name':store_names,
        'food': food})

# 食材詳細
@login_required
def food_detail(request, food_id):
    store = request.user
    food = get_object_or_404(Food, id=food_id, store=store)
    food.expiration_date_jp = food.expiration_date.strftime('%Y年%m月%d日')
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    return render(request, 'foods/food_detail.html', {
        'current_date': current_date,
        'work_status':work_status,
        'store_name':store_names,
        'food': food})


#ログアウト
@login_required
def logout_confirm(request):
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    return render(request, 'foods/logout.html',{
        'work_status':work_status,
        'store_name':store_names,})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home') 

#食材削除(食材を利用した商品ありの場合)
@login_required
def ingredient_confirm_delete(request, food_id):
    store = request.user
    food = get_object_or_404(Food, id=food_id, store=store)
    associated_products = Product.objects.filter(ingredients=food)
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    if associated_products.exists():
        if request.method == 'POST' and 'confirm_delete' in request.POST:
            associated_products.delete()
            food.delete()
            messages.success(request, "選択した食材と関連する商品が削除されました。")
            return redirect('food_list')
        return render(request, 'foods/ingredient_confirm_delete.html', {
            'current_date': current_date,
            'work_status':work_status,
            'store_name':store_names,
            'food': food,
            'associated_products': associated_products
        })

    return redirect('food_delete', food_id=food_id)

#メインページ
def main_page(request):
    current_date = datetime.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    return render(request, 'foods/main_page.html', {'current_date': current_date, 'work_status': work_status, 'store_name': store_names,})




