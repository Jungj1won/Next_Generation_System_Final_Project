from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # 회원가입
    path('login/', views.login, name='login'),          # 로그인
    path('logout/', views.logout, name='logout'),       # 로그아웃
    path('index/', views.index, name='index'),          # 메인 페이지
]
