from django.shortcuts import render
from .models import Post


def index(request):
    posts = Post.objects.all().order_by('-pk')      #모든 post 레코드를 가져옴.


    return render(
        request,
        'blog/index.html',
        {
            'posts' : posts,
        }
    )