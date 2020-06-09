from django import forms
from .models import ArticlePost

# 寫文章表單類
class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost # 模型數據來源
        fields = ('title', 'body', 'tags', 'avatar') # 表單套用字段








