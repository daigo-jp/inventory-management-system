from django.shortcuts import render, redirect
from menu.models import Product
from foods.models import Food
from sales.models import Sales  # Salesモデルをインポート
from django.db.models import Q
from datetime import date
from django.contrib.auth.decorators import login_required

@login_required
def order_confirmation(request):
    # 注文確認ページでセッションの注文リストを取得
    current_date = date.today().strftime('%Y年%m月%d日')  # 現在の日付を取得
    work_status = request.session.get('work_status', "営業終了")

    order_list = request.session.get('order_list', [])
    total_price = sum(item['subtotal'] for item in order_list)  # 合計金額を計算
    return render(request, 'order/order_confirmation.html', {
        'work_status': work_status,
        'current_date': current_date,
        'order_list': order_list,
        'total_price': total_price,
    })

@login_required
def product_list(request):
    store = request.user 
    query = request.GET.get('q')
    
    if query:
        # 食材名または種類でフィルタリング
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

@login_required
def order(request):
    current_date = date.today().strftime('%Y年%m月%d日')  # 現在の日付を取得
    work_status = request.session.get('work_status', "営業終了")
    
    if request.method == 'POST':
        order_list = request.session.get('order_list', [])

        # 「注文する」ボタンが押された場合、注文リストが空ならエラーメッセージを表示
        if 'order_submit' in request.POST:
            if not order_list:
                error_message = "注文リストが空欄です。"
                products = Product.objects.filter(store=request.user)
                return render(request, 'order/order.html', {
                    'work_status': work_status,
                    'current_date': current_date,
                    'products': products,
                    'order_list': order_list,
                    'total_price': sum(item.get('subtotal', 0) for item in order_list),
                    'error_message': error_message,
                })
            return redirect('order_confirmation')  # 通常の注文確認ページへリダイレクト
        
        
        # 注文リストに商品を追加する機能
        if 'add_product' in request.POST:
            product_id = request.POST.get('add_product')
            quantity = int(request.POST.get(f'quantity_{product_id}', 1))
            order_list = request.session.get('order_list', [])
            try:
                product = Product.objects.get(id=product_id)
                # 商品ごとの食材が足りているか確認
                insufficient_foods = []
                for ingredient in product.productingredient_set.all():
                    food = ingredient.food  # 食材
                    required_quantity = ingredient.quantity * quantity  # 必要な食材量
                    if food.quantity < required_quantity:
                        insufficient_foods.append(food.name)  # 足りない食材をリストに追加
                
                if insufficient_foods:
                    # 足りない食材がある場合はエラーメッセージを表示
                    error_message = f"「{product.name}」は現在、食材不足で注文できません。<br><br>不足している食材：{'、'.join(insufficient_foods)}"
                    return render(request, 'order/order.html', {
                        'work_status': work_status,
                        'current_date': current_date,
                        'products': Product.objects.filter(store=request.user),
                        'order_list': order_list,
                        'total_price': sum(item.get('subtotal', 0) for item in order_list),
                        'error_message': error_message,
                    })

                # 食材が足りる場合、注文リストに追加
                for item in order_list:
                    if item['product_id'] == product.id:
                        item['quantity'] += quantity
                        item['subtotal'] = item['price'] * item['quantity']
                        break
                else:
                    order_item = {
                        'product_id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'quantity': quantity,
                        'subtotal': product.price * quantity,
                    }
                    order_list.append(order_item)

                request.session['order_list'] = order_list  # セッションに保存
            except Product.DoesNotExist:
                # 商品が存在しない場合のエラーハンドリング
                pass

        # 注文リストの削除機能
        elif 'remove_product' in request.POST:
            product_id = int(request.POST.get('remove_product'))

            order_list = request.session.get('order_list', [])
            order_list = [item for item in order_list if item['product_id'] != product_id]
            request.session['order_list'] = order_list  # セッションに保存
        
        return redirect('order')  # 再描画

    # 商品の取得（ログインしているユーザーに関連する商品）
    products = Product.objects.filter(store=request.user)

    # 検索機能を追加
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(category__icontains=query))
    
    # セッションに保存された注文リストの取得
    order_list = request.session.get('order_list', [])
    total_price = sum(item.get('subtotal', 0) for item in order_list)  # 合計金額を計算

    return render(request, 'order/order.html', {
        'work_status': work_status,
        'current_date': current_date,
        'products': products,
        'order_list': order_list,
        'total_price': total_price,
        'error_message': None,  # エラーメッセージを表示しない
    })

@login_required
def order_complete(request):
    # 営業状態を取得
    current_date = date.today().strftime('%Y年%m月%d日')  # 現在の日付を取得
    work_status = request.session.get('work_status', "営業終了")
    
    # 注文完了処理
    order_list = request.session.get('order_list', [])
    
    # 注文内容を元に、食材の数量を減らす
    for item in order_list:
        try:
            product = Product.objects.get(id=item['product_id'])
            
            # 売上記録をSalesモデルに保存
            Sales.objects.create(
                product=product,
                quantity=item['quantity'],
                price=item['price'],
            )
            
            # ProductIngredientを通じて、商品の各食材を取得
            for ingredient in product.productingredient_set.all():
                food = ingredient.food  # 食材
                ingredient_quantity = ingredient.quantity  # 商品1つ当たりの食材の使用量
                
                # 注文数に応じて食材の数量を減らす
                food.quantity -= ingredient_quantity * item['quantity']
                
                # 在庫数が0未満にならないように制御
                if food.quantity < 0:
                    food.quantity = 0
                
                food.save()  # 食材の在庫を保存

        except Product.DoesNotExist:
            pass  # 商品が存在しない場合は何もしない
    
    # 注文完了後に注文リストをクリア
    request.session['order_list'] = []
    
    return render(request, 'order/order_complete.html', {
        'work_status': work_status,
        'current_date': current_date,
    })
