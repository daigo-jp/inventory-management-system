from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sales
from .forms import SalesForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from menu.models import Product
from datetime import date
from django.db.models import Sum, FloatField
from django.db.models.functions import TruncDate
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

            # 商品の価格を自動的に設定
            sale.price = product.price

            # 商品の在庫数を計算してチェック
            stock = product.get_stock()
            if sale.quantity > stock:
                messages.error(request, f"販売数量が在庫({stock})を超えています")
                return redirect('sales_create')  # エラー時は売上登録ページにリダイレクト
            else:
                # 各食材の数量を減算
                for ingredient in product.productingredient_set.all():
                    ingredient.food.quantity -= sale.quantity * ingredient.quantity
                    ingredient.food.save()

                sale.save()
                messages.success(request, "売上が正常に記録されました")
                return redirect('sales_list')  # 成功時に売上一覧ページにリダイレクト
    else:
        form = SalesForm(user=request.user)

    return render(request, 'sales/sales_create.html', {
        'form': form,
        'current_date': current_date,
        'work_status': work_status,  
        'store_name': store_names, 
        })


@login_required
def sales_list(request):
    sales = Sales.objects.filter(product__store=request.user).order_by('-sale_date')
    current_date = date.today().strftime('%Y年%m月%d日')  
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')

    low_stock_products = [
        product for product in Product.objects.filter(store=request.user)
        if product.get_stock() <= 10
    ]

    # 日付ごとに売上をグループ化
    grouped_sales = {}
    for sale in sales:
        sale_date = sale.sale_date.date()
        if sale_date not in grouped_sales:
            grouped_sales[sale_date] = []
        grouped_sales[sale_date].append(sale)
    
     # 最新の日付順に並び替え（辞書のキーを降順ソート）
    grouped_sales = dict(sorted(grouped_sales.items(), key=lambda x: x[0], reverse=True))
    
    return render(request, 'sales/sales_list.html', {
        'sales': sales,
        'grouped_sales': grouped_sales,
        'low_stock_products': low_stock_products,
        'current_date': current_date,
        'work_status': work_status,  
        'store_name': store_names, 
    })
    
@login_required
def get_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
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

    # グラフ作成
    chart = graph.Plot_Graph(dates, revenues)

    return render(request, 'sales/sales_graph.html', {
        'chart': chart,
        'current_date': current_date,
        'work_status': work_status,  
        'store_name': store_names, 
    })