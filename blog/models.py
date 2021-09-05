from django.db import models
from django.contrib.auth.models import User
import os


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # CASCADE

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # 게시물 제목 나타내기, [pk] title
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