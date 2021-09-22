from django.shortcuts import render, redirect           # redirect for form_valid()
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # LRM for login, UPTM for user permission
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.core.exceptions import PermissionDenied     # only writer can update his post
from django.utils.text import slugify                   # for slugify()


# CBV 방식
class PostList(ListView):
    model = Post
    ordering = '-pk'    # 최신순(pk 내림차순)

    def get_context_data(self, **kwargs):   # ListView 의 멤버함수 get_context_data 오버라이딩, CBV에서 template으로 추가 인자를 넘길 때 사용.
        context = super(PostList, self).get_context_data()  # 기존 기능 유지
        # 두 가지 정보 추가
        context['categories'] = Category.objects.all()      # no_category 포함 모든 카테고리 이름 가져오고, 해당 개수 또한 가져옴.
        context['no_category_post_count'] = Post.objects.filter(category=None).count()  # 미분류 카테고리 개수 가져옴.
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post        # 템플릿 파일 post_form.html

    # post 모델에 사용할 필드명을 리스트로 추가. (tags) 는 템플릿에서 직접 추가하였음.
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):    # 관리자, 스태프만 해당 페이지 접근 가능
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form) # author가 담긴 form 임시 저장. 이후 tag까지 추가한 뒤 return

            tags_str = self.request.POST.get('tags_str')        # 템플릿 파일 post_form.html의 'tags_str'에 담긴 input을 가져와
            if tags_str:    # if there is one or more tags
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')     # type(tags_list) is list

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)     # if t exists then bring it else make it
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)   # slug 값을 만들어야함. allow_unicode=True means 한글 지원
                        tag.save()
                    self.object.tags.add(tag)   # 해당 게시물 필드에 tag 추가. *** 이미 response에 form저장했으므로 해당 게시물 form 필드에 tag 추가.

            return response
        else:
            return redirect('/blog')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/post_update_form.html'        # CreateView, UpdateView는 모델명_form.html이 default template

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():   # if tag already exists, fill ['tags_str_default'] with tags that already exists
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')        # 템플릿 파일 post_form.html의 'tags_str'에 담긴 input을 가져와
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:  # 로그인한 유저가 해당 댓글 작성자가 맞는 경우
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

# FBV 방식
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',  # post_list.html을 사용하므로, PostList 에서 context로 정의했던 부분을 딕셔너리 형태로 직접 정의해야 함.
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':                # url을 통해 get으로 접근불가, submit을 통한 post 방식일때만
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)   # 바로 저장하지 말고, 인스턴스만 가져온다. 그 후 comment에 작성자, post를 담은 뒤 저장
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        return PermissionDenied