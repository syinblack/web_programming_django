from django.db import models

#Post 모델 만들기.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #autor:

    # 게시물 제목 나타내기, [pk] title
    def __str__(self):
        return f'[{self.pk}] {self.title}'