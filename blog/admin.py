from django.contrib import admin                # 기본 장고 세팅
from markdownx.admin import MarkdownxModelAdmin # 관리자 페이지에서도 마크다운 사용
from .models import Post, Category, Tag         # models.py 에서 정의한 클래스들 가져오기.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}  # Category class의 name을 slug 로 변환한다.


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


# 관리자 페이지에 클래스 등록
admin.site.register(Post, MarkdownxModelAdmin)  # 관리자 페이지에서도 마크다운 적용
admin.site.register(Category, CategoryAdmin)    # category 클래스를 categoryAdmin 으로 커스터마이징하여 등록
admin.site.register(Tag, TagAdmin)
