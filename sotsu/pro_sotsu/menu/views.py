from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductIngredient
from .forms import ProductForm
from foods.models import Food
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date

#商品一覧
@login_required
def product_list(request):
    store = request.user 
    query = request.GET.get('q')
    
    if query:
        products = Product.objects.filter(
            store=store
        ).filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )
    else:
        # 全ての商品を取得
        products = Product.objects.filter(store=store)
    
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    
    return render(request, 'menu/product_list.html', {
        'products': products,
        'query': query,
        'current_date':current_date,
        'work_status': work_status,
        'store_name': store_names
    })
    
#商品登録
@login_required
def product_create(request):
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    if request.method == 'POST':
        form = ProductForm(request.POST, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = request.user

            # 重複チェック
            if Product.objects.filter(name=product.name, store=request.user).exists():
                messages.error(request, f"商品名 '{product.name}' は既に登録されています。別の名前を入力してください。")
                return redirect('product_create')

            total_cost = 0
            #has_valid_ingredient = False
            ingredients = form.cleaned_data.get('ingredients', [])
            if not ingredients:
                messages.error(request, "少なくとも1つの食材を選択してください。")
                return redirect('product_create')

            for food in ingredients:
                quantity_str = request.POST.get(f'quantity_{food.id}', '').strip()
                if not quantity_str:
                    messages.error(request, f"{food.name}の数量を入力してください。")
                    return redirect('product_create')

                try:
                    quantity = int(quantity_str)
                    if quantity > 0:
                        cost = food.cost * quantity
                        total_cost += cost
                        #has_valid_ingredient = True
                    else:
                        messages.error(request, f"{food.name}の数量は1以上である必要があります。")
                        return redirect('product_create')
                except ValueError:
                    messages.error(request, f"{food.name}の数量は有効な数値である必要があります。")
                    return redirect('product_create')

            if product.price < total_cost:
                messages.error(request, f"商品の価格は材料の合計コスト（{total_cost}円）以上である必要があります。")
                return redirect('product_create')

            product.save()

            ProductIngredient.objects.filter(product=product).delete()
            for food in ingredients:
                quantity = int(request.POST.get(f'quantity_{food.id}', '0'))
                ProductIngredient.objects.create(
                    product=product,
                    food=food,
                    quantity=quantity
                )

            messages.success(request, f"商品 '{product.name}' が正常に登録されました。")
            return redirect('product_list')
        else:
            messages.error(request, "食材を選択してください")
            print("デバッグ: フォームエラー - ", form.errors)
    else:
        form = ProductForm(user=request.user)

    ingredients = Food.objects.filter(store=request.user)
    print("デバッグ: 取得した食材情報 - ", [ingredient.name for ingredient in ingredients])

    return render(request, 'menu/product_create.html', {
        'current_date': current_date,
        'work_status':work_status, 
        'store_name': store_names,
        'form': form,
        'ingredients': ingredients
    })


#商品編集
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, store=request.user)
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = request.user

            # 合計原価と商品の価格をチェック
            total_cost = 0
            ingredients = form.cleaned_data.get('ingredients', [])
            has_valid_ingredient = False

            for food in ingredients:
                quantity = request.POST.get(f'quantity_{food.id}', '0')
                try:
                    quantity = int(quantity)
                    if quantity > 0:
                        cost = food.cost * quantity
                        total_cost += cost
                        has_valid_ingredient = True
                except ValueError:
                    continue

            # 商品の価格が合計原価以上であるかをチェック
            if product.price < total_cost:
                messages.error(request, f"商品の価格は材料の合計コスト（{total_cost}円）以上である必要があります。")
                return redirect('product_edit', pk=pk)

            product.save()

            # ProductIngredientを更新
            ProductIngredient.objects.filter(product=product).delete()
            for food in ingredients:
                quantity = int(request.POST.get(f'quantity_{food.id}', '0'))
                ProductIngredient.objects.create(
                    product=product,
                    food=food,
                    quantity=quantity
                )

            messages.success(request, f"商品 '{product.name}' が正常に編集されました。")
            return redirect('product_list')
        else:
            messages.error(request, "フォームが無効です。")
            print("デバッグ: フォームエラー - ", form.errors)  # デバッグ
    else:
        form = ProductForm(instance=product, user=request.user)

    ingredients = Food.objects.filter(store=request.user)
    product_ingredients = [
        {
            'food': ingredient,
            'quantity': ProductIngredient.objects.filter(product=product, food=ingredient).first().quantity if ProductIngredient.objects.filter(product=product, food=ingredient).exists() else 0
        }
        for ingredient in ingredients
    ]


    return render(request, 'menu/product_edit.html', {
        'current_date': current_date,
        'work_status':work_status, 
        'store_name': store_names,
        'form': form,
        'ingredients': product_ingredients,        
    })

#商品削除
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, store=request.user)
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'menu/product_delete.html', {
        'current_date': current_date,
        'work_status':work_status, 
        'store_name': store_names,
        'product': product})

#商品情報
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, store=request.user)
    ingredients = product.productingredient_set.all()
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    
    # 各食材の合計原価を計算して、ingredientに追加する
    ingredient_details = []
    total_cost = 0
    for ingredient in ingredients:
        cost_total = ingredient.food.cost * ingredient.quantity
        ingredient_details.append({
            'name': ingredient.food.name,
            'cost': ingredient.food.cost,
            'quantity': ingredient.quantity,
            'cost_total': cost_total
        })
        total_cost += cost_total
    
    return render(request, 'menu/product_detail.html', {
        'product': product,
        'ingredients': ingredient_details,
        'current_date': current_date,
        'work_status':work_status, 
        'store_name': store_names,
        'total_cost': total_cost
    })
