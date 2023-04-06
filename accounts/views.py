from django.shortcuts import render, redirect
from .models import AccountsModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model  # 사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# 임시 홈


def home(request):

    # context = {'message': '안녕하세요, 테스트 홈페이지입니다.'}

    user = request.user.is_authenticated
    if user:
        # return redirect('/tweet')
        return render(request, 'my_test.html')
        return render('../my_test.html')
    else:
        return redirect('/sign-in')


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        # bio = request.POST.get('bio', '')

        if password != password2:
            # 패스워드가 같지 않다고 알람
            return render(request, 'accounts/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'accounts/signup.html', {'error': '사용자 이름과 비밀번호는 필수 값 입니다!'})

            exist_user = get_user_model().objects.filter(username=username)

            if exist_user:
                # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
                return render(request, 'accounts/signup.html', {'error': '사용자가 존재합니다'})
            else:
                AccountsModel.objects.create_user(
                    username=username, password=password, email=email)  # bio=bio)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'accounts/signin.html', {'error': '유저이름 혹은 패스워드를 확인 해 주세요'})
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'accounts/signin.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = AccountsModel.objects.all().exclude(username=request.user.username)
        return render(request, 'accounts/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = AccountsModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')
