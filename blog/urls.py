from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.single_post_page),     # blog/숫자 형태일때는 views.single_post_page함수로 전달
]
