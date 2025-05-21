from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now 
from datetime import date
from .models import WorkDatetime

#営業開始確認
@login_required
def work_start_check(request):
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    return render(request, 'work/work_start_check.html', {
        'work_status': work_status,
        'current_date': current_date,
        'store_name': store_names
    })

#営業開始完了
@login_required
def work_start_ok(request):
    store_name = request.user 
    work_datetime, created = WorkDatetime.objects.get_or_create(store_name=store_name)
    work_datetime.work_start_time = now()
    work_datetime.save()

    request.session['work_status'] = "営業中"
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    return render(request, 'work/work_start_ok.html', {
        'work_status': work_status,
        'store_name': store_names
    })


# 営業終了確認
@login_required
def work_end_check(request):
    current_date = date.today().strftime('%Y年%m月%d日')
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    return render(request, 'work/work_end_check.html', {
        'work_status': work_status,
        'current_date': current_date,
        'store_name': store_names
    })


# 営業終了完了
@login_required
def work_end_ok(request):
    store_name = request.user
    work_datetime = WorkDatetime.objects.get(store_name=store_name)
    work_datetime.work_end_time = now()
    work_datetime.save()

    request.session['work_status'] = "営業終了"
    work_status = request.session.get('work_status', "営業終了")
    store_names = request.session.get('store_name')
    return render(request, 'work/work_end_ok.html', {
        'work_status': work_status,
        'store_name': store_names
    })