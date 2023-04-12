from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-in/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
]

# name= 은 템플릿 썼을 때에 필수
