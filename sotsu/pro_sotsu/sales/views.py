from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction  # ★ データベース操作の安全性を高めるために追加
from django.db.models import Sum
from django.db.models.functions import TruncDate
from datetime import date
from .models import Sales
from .forms import SalesForm
from menu.models import Product
from . import graph

@login_required
def sales_create(request):
    store = request.user 
    current_date = date.today().strftime('%Y年%m月%d日') 
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    
    if request.method == 'POST':
        form = SalesForm(request.POST, user=request.user)
        if form.is_valid():
            sale = form.save(commit=False)
            product = sale.product
            sale.price = product.price # 商品価格を自動設定

            # 在庫チェック
            stock = product.get_stock()
            if sale.quantity > stock:
                messages.error(request, f"販売数量が在庫({stock})を超えています")
                return redirect('sales_create')
            
            try:
                # ★ トランザクション処理を追加
                #   売上記録と在庫減算の処理をひとまとめにする
                #   途中でエラーが起きても、すべての変更が取り消されデータが守られます
                with transaction.atomic():
                    # 各食材の数量を減算
                    for ingredient in product.productingredient_set.all():
                        ingredient.food.quantity -= sale.quantity * ingredient.quantity
                        ingredient.food.save()
                    
                    # 売上を保存
                    sale.save()

                messages.success(request, "売上が正常に記録されました")
                return redirect('sales_list')
            except Exception as e:
                # 万が一、処理中にエラーが発生した場合
                messages.error(request, f"処理中にエラーが発生しました: {e}")
                return redirect('sales_create')

    else:
        form = SalesForm(user=request.user)

    context = {
        'form': form,
        'current_date': current_date,
        'work_status': work_status, 
        'store_name': store_names, 
    }
    return render(request, 'sales/sales_create.html', context)


@login_required
def sales_list(request):
    sales = Sales.objects.filter(product__store=request.user).order_by('-sale_date')
    current_date = date.today().strftime('%Y年%m月%d日') 
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')

    # Note: 商品数が増えると、この処理は遅くなる可能性があります
    #       全商品の在庫を一つずつチェックしているためです。
    low_stock_products = [
        product for product in Product.objects.filter(store=request.user)
        if product.get_stock() <= 10
    ]

    grouped_sales = {}
    for sale in sales:
        sale_date = sale.sale_date.date()
        if sale_date not in grouped_sales:
            grouped_sales[sale_date] = []
        grouped_sales[sale_date].append(sale)
    
    grouped_sales = dict(sorted(grouped_sales.items(), key=lambda x: x[0], reverse=True))
    
    context = {
        'grouped_sales': grouped_sales,
        'low_stock_products': low_stock_products,
        'current_date': current_date,
        'work_status': work_status, 
        'store_name': store_names, 
    }
    return render(request, 'sales/sales_list.html', context)
    
@login_required
def get_stock(request, product_id):
    # ★ セキュリティ強化: ログイン中のユーザーが所有する商品のみを対象にする
    product = get_object_or_404(Product, id=product_id, store=request.user)
    stock = product.get_stock() 
    return JsonResponse({'stock': stock})


@login_required
def sales_graph(request):
    current_date = date.today().strftime('%Y年%m月%d日') 
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')

    daily_sales = (
        Sales.objects.filter(product__store=request.user) 
        .annotate(sale_day=TruncDate('sale_date')) 
        .values('sale_day') 
        .annotate(total_revenue=Sum('total_cost'))
        .order_by('sale_day')
    )

    dates = [data['sale_day'].strftime('%Y-%m-%d') for data in daily_sales]
    revenues = [int(data['total_revenue']) for data in daily_sales] 

    # ▼▼▼ グラフ作成関数を新しいものに変更 ▼▼▼
    chart = graph.Plot_Enhanced_Graph(dates, revenues)

    context = {
        'chart': chart,
        'current_date': current_date,
        'work_status': work_status, 
        'store_name': store_names, 
    }
    return render(request, 'sales/sales_graph.html', context)