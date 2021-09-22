from django.urls import path
from . import views     # 같은 폴더의 views.py 함수 사용하여 url 연결

urlpatterns = [
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),

    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/new_comment/', views.new_comment),
    path('<int:pk>/', views.PostDetail.as_view()),              # blog/숫자 형태일때는 views.single_post_page 함수로 전달
    path('', views.PostList.as_view()),                         # blog 랜딩 페이지
]
