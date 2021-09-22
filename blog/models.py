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
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField() # models.TextField()

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