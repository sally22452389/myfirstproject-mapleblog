from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

# 文章評論
class Comment(MPTTModel):
    # 被評論的文章
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # 評論的發布者
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    # mptt結構
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    # 評論給誰 str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )
    # body = models.TextField()
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    # class Meta:
    #    ordering = ('created',)
    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]
