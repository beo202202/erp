from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 임시
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-in/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
]
