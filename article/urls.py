# article/urls.py
from django.urls import path
from . import views  # 같은 폴더 내 views.py import

urlpatterns = [
    path('articlereg/', views.articlereg, name='articlereg'),  # 크롤링/DB저장
    path('subject/', views.subject, name='subject'),           # 주제별 논문 화면
]