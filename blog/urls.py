from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.single_post_page),     # blog/숫자 형태일때는 views.single_post_page함수로 전달
    path('', views.index),
]
