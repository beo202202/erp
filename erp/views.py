from django.shortcuts import render, redirect
from .forms import ProductForm, InboundForm
from .models import Product, Inbound
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import datetime

# Create your views here.

# view.py


@transaction.atomic
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # code값이 이미 있다면 form창에서 경고를 불러주는 듯
            # commit=False 옵션으로 데이터베이스에 바로 저장하지 않음
            product = form.save(commit=False)
            product.author = request.user
            product.save()  # 저장되기 전에 추가 작업을 수행할 수 있음
            # 저장이 완료되면 success 페이지로 이동
            return redirect('/product-success')
            # 성공하셨습니다! 글자만 보여주고 주소는 같음.
            # return HttpResponse('성공하셨습니다!')
    else:
        form = ProductForm()
    return render(request, 'erp/product_create.html', {'form': form})


@login_required
def product_list(request):
    # 자기가 등록 한 상품의 리스트를 볼 수 있는 view
    if request.method == 'GET':
        user = request.user
        print(f"{user=}")
        if user:
            user_product = Product.objects.filter(
                author_id=user).order_by('code')
            # 뭔가 수정해야함.
            return render(request, 'erp/product_list.html', {'products': user_product})
        else:
            return redirect('/sign-in')


@login_required
def product_success(request):
    # 등록 된 상품의 성공을 볼 수 있는 view
    return render(request, 'erp/product_success.html')


@login_required
@transaction.atomic
def product_all_delete(request):
    # Product 테이블의 모든 레코드 삭제
    Product.objects.all().delete()
    return redirect('/product-list')


@login_required
@transaction.atomic
def product_my_all_delete(request):
    # 현재 접속한 사람의 레코드 삭제
    user = request.user
    Product.objects.filter(author_id=user).delete()
    return redirect('/product-list')


# views.py
@login_required
@transaction.atomic
def inbound_create(request):
    # 상품 입고 view
    # 입고 기록 생성
    if request.method == 'POST':
        form = InboundForm(request.POST)
        if form.is_valid():
            inbound = form.save(commit=False)
            inbound.inbound_date = datetime.now()
            inbound.save()
            # 성공하셨습니다! 글자만 보여주고 주소는 같음.
            return HttpResponse('성공하셨습니다!')
            # 입/출고 합산 기능 연결...
            # return redirect('inbound-list')
    else:
        form = InboundForm()
    return render(request, 'erp/inbound_create.html', {'form': form})
