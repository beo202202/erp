from django.shortcuts import render, redirect
from .forms import ProductForm, InboundForm, OutboundForm
from .models import Product, Inbound, Outbound, Inventory
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib import messages

# get_object_or_404()를 써볼까?
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
            # 입/출고 합산 기능 연결
            return redirect('/inventory/')
            # 성공하셨습니다! 글자만 보여주고 주소는 같음.
            return HttpResponse('입고 성공하셨습니다!')
    else:
        form = InboundForm()
    return render(request, 'erp/inbound_create.html', {'form': form})


@login_required
def outbound_create(request, product_id):
    # 선택한 상품을 가져옴
    product = get_object_or_404(Product, code=product_id)
    # 출고 기록 생성
    outbound = Outbound(product=product)

    if request.method == 'POST':
        form = OutboundForm(request.POST, instance=outbound)
        if form.is_valid():
            # outbound.product = product
            outbound = form.save(commit=False)

            products = Product.objects.all()

            # 수량이 없으면 경고하기
            for producta in products:
                inbound_total_quantity = Inbound.objects.filter(product_id=product_id).aggregate(
                    total_quantity=Sum('quantity'))['total_quantity'] or 0

                producta.quantity_sum = inbound_total_quantity

            outbound_quantity = form.cleaned_data['quantity']

            if producta.quantity_sum < outbound_quantity:
                return HttpResponse('출고할 수 있는 수량이 충분하지 않습니다.')

            # 출고 기록 저장
            outbound.save()
            product.save()
            # 인베토리로 연결하기
            return redirect('/product-success/')
    else:
        form = OutboundForm(instance=outbound)
    return render(request, 'erp/outbound_create.html', {'form': form, 'product_id': product_id})


@login_required
def inventory(request):
    # """
    # inbound_create, outbound_create view에서 만들어진 데이터를 합산합니다.
    # Django ORM을 통하여 총 수량, 가격등을 계산할 수 있습니다.
    # """
    # 총 입고 수량, 가격 계산

    products = Product.objects.all()

    for product in products:
        # print(product)
        # 총 입고 수량 계산
        inbound_total_quantity = Inbound.objects.filter(product_id=product).aggregate(
            total_quantity=Sum('quantity'))['total_quantity'] or 0
        # 총 입고 비용 계산
        inbound_total_amount = Inbound.objects.filter(product_id=product).aggregate(
            total_amount=Sum('amount'))['total_amount'] or 0
        # 총 출고 수량 계산
        outbound_total_quantity = Outbound.objects.filter(product_id=product).aggregate(
            total_quantity=Sum('quantity'))['total_quantity'] or 0
        # 총 출고 수량 계산
        outbound_total_amount = Outbound.objects.filter(product_id=product).aggregate(
            total_amount=Sum('amount'))['total_amount'] or 0

        # 현재 수량 계산
        current_quantity = inbound_total_quantity - outbound_total_quantity

        # Product 객체에 수량 정보 추가
        product.inbound_total_quantity = inbound_total_quantity
        product.inbound_total_amount = inbound_total_amount
        product.outbound_total_quantity = outbound_total_quantity
        product.outbound_total_amount = outbound_total_amount
        product.current_quantity = current_quantity

    return render(request, 'erp/inventory.html', {'products': products})
