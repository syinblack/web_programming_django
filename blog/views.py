from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post

# FBV방식 (이제 사용안함.)
"""def index(request):
    posts = Post.objects.all().order_by('-pk')      # 모든 post 레코드를 가져옴.


    return render(
        request,
        'blog/post_list.html',
        {
            'posts' : posts,
        }
    )


def single_post_page(request, pk):      # pk는 데이터베이스에서 데이터를 불러오기 위함.
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/post_detail.html',
        {
            'post' : post,
        }
    )
"""