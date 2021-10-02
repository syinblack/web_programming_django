from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # category 에 대한 고유 url 설정
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)    # allow_unicode = True : 한글 허용

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'  # 복수명 수동 설정


class Post(models.Model):
    title = models.CharField(max_length=50)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()  # models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # many to one field
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # on_delete : 해당 작성자가 삭제 되었을 때 관련된 게시물 처리 정책
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # one to one field
    tags = models.ManyToManyField(Tag, blank=True)

    # 게시물 제목 나타내기 : ex [num] title :: 작성자
    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    # 게시물 이름 표시
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 게시물 확장자 표시
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    # 마크다운 필드값 html 변환
    def get_content_markdown(self):
        return markdown(self.content)

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():      # 소셜 로그인 계정의 아바타 url 이 있을 경우 가져온다.
            return self.author.socialaccount_set.first().get_avatar_url()
        else:   # 없을 경우 doitdjango.com/avatar 에서 생성한 프로젝트 id, pw를 통해 고유 아바타 생성
            return f'https://doitdjango.com/avatar/id/311/e7a558bbb4069d38/svg/{self.author.username}' # email도 가능하지만, 존재하지 않을 수 있음

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/311/e7a558bbb4069d38/svg/{self.author.username}'