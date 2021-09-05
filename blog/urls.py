from django.urls import path
from . import views

urlpatterns = [
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),     # blog/숫자 형태일때는 views.single_post_page 함수로 전달
]
