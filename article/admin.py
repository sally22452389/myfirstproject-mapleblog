from django.contrib import admin
from .models import ArticlePost, ArticleColumn


# Register your models here.

admin.site.register(ArticlePost) # 文章發送
admin.site.register(ArticleColumn) # 文章欄目



