from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 임시
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    # path('user/foloow/<int:id>', views.user_follow, name='user-follow'),
]
