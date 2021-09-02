from django.shortcuts import render
from .models import Post


def index(request):
    posts = Post.objects.all().order_by('-pk')      # 모든 post 레코드를 가져옴.


    return render(
        request,
        'blog/index.html',
        {
            'posts' : posts,
        }
    )


def single_post_page(request, pk):      # pk는 데이터베이스에서 데이터를 불러오기 위함.
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post' : post,
        }
    )
