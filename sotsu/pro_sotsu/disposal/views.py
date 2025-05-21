from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from django.contrib import messages
from .forms import DisposalForm
from .models import Disposal

#ロス商品一覧
@login_required
def disposal_manage(request):
    current_date = date.today().strftime('%Y年%m月%d日') 
    work_status = request.session.get('work_status', "営業終了")
    store = request.user
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'id') 
    order = request.GET.get('order', 'asc')
 
    disposals = Disposal.objects.filter(store=store)
    if query:
        disposals = disposals.filter(
            Q(disposal_menu__name__icontains=query) | Q(category__icontains=query) | Q(disposal_date__icontains=query)
        )
    
    
    if order == 'asc':
        disposals = disposals.order_by(sort_by)
    elif order == 'desc':
        disposals = disposals.order_by('-' + sort_by)

    for disposal in disposals:
        disposal.disposal_date_jp = disposal.disposal_date.strftime('%Y年%m月%d日')

    return render(request, 'disposal/disposal_manage.html', {
        'current_date': current_date,
        'work_status':work_status,  
        'disposals': disposals,
        'query': query,
        'sort_by': sort_by,
        'order': order,
    })

#ロス登録
@login_required
def disposal_register(request):
    store = request.user
    current_date = date.today().strftime('%Y年%m月%d日')  
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    
    if request.method == 'POST':
        form = DisposalForm(request.POST, user=request.user)
        if form.is_valid():
            disposal = form.save(commit=False)
            disposal.store = request.user 
            disposal.save()
            return redirect('disposal_manage')

        else:
            print(form.errors)  # エラーメッセージを確認
            print(form.cleaned_data)  # フォームのデータを確認
    else:
        form = DisposalForm(user=store)  # GET リクエスト時も user を渡す

    return render(request, 'disposal/disposal_register.html', {
        'current_date': current_date,
        'work_status': work_status,  
        'store_name': store_names,   
        'form': form
    })
    
#ロス編集
@login_required
def disposal_edit(request, disposal_id):
    store = request.user
    disposal = get_object_or_404(Disposal, id=disposal_id, store=store)
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了") 
    store_names = request.session.get('store_name')   

    if request.method == 'POST':
        form = DisposalForm(request.POST, instance=disposal, user=store)
        if form.is_valid():
            disposal = form.save(commit=False)
            disposal.store = store
            disposal.save()
            return redirect('disposal_manage')
        else:
            print(form.errors)  # エラーをデバッグ
    else:
        form = DisposalForm(instance=disposal, user=store)

    return render(request, 'disposal/disposal_edit.html', {
        'current_date': current_date,
        'form': form,
        'disposal': disposal,
        'work_status':work_status,
        'store_name': store_names
    })
   
#ロス削除 
@login_required
def disposal_delete(request, disposal_id):
    disposal = get_object_or_404(Disposal, id=disposal_id, store=request.user)
    current_date = date.today().strftime('%Y年%m月%d日') 
    work_status = request.session.get('work_status', "営業終了") 
    store_names = request.session.get('store_name')   
    if request.method == 'POST':
        disposal.delete()
        messages.success(request, f"ロス '{disposal.disposal_menu}' が削除されました。")
        return redirect('disposal_manage')
    
    return render(request, 'disposal/disposal_delete.html', {
        'disposal': disposal,
        'current_date': current_date,
        'work_status':work_status,
        'store_name': store_names})

#ロス情報
@login_required
def disposal_detail(request, disposal_id):
    store = request.user
    disposal = get_object_or_404(Disposal, id=disposal_id, store=store)  
    disposal.disposal_date_jp = disposal.disposal_date.strftime('%Y年%m月%d日')
    
    current_date = date.today().strftime('%Y年%m月%d日') 
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    
    return render(request, 'disposal/disposal_detail.html', {
        'disposal': disposal,
        'current_date': current_date,
        'work_status':work_status,
        'store_name': store_names})

