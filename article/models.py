from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager #標籤
from PIL import Image
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.utils import timezone

# Create your models here.

# 文章欄目 專欄
class ArticleColumn(models.Model):

    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

#博客文章數據模型
class ArticlePost(models.Model):
    # 參數on_delete用於指定數據刪除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # models.CharField為字符字段，用於保存較短的字符
    title = models.CharField(max_length=100)

    # 保存大量文本用TextField 
    body = models.TextField()

    # 參數default=timezone.now指定其在創建數據時將寫入當前時間
    created = models.DateTimeField(default=timezone.now)

    # 參數auto_now=True指定每次更新時自動寫入當前時間
    updated = models.DateTimeField(auto_now=True)

    # 文章瀏覽量 PositiveIntegerField存儲正整數的字段 初始=0
    total_views = models.PositiveIntegerField(default=0)

    # 文章欄目的"一對多"外鍵
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 文章標籤
    tags = TaggableManager(blank=True)  

    # 文章標題圖
    avatar = ProcessedImageField(
        upload_to='article/%Y%m%d',
        processors=[ResizeToFit(width=400)],
        blank=True,
        format='JPEG',
        options={'quality': 100},
    )

    # 點讚數統計
    likes = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # 用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定寬度縮放圖片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    # 內部類class Meta用於給model定義元數據
    class Meta:
        # ordering指定模型返回的數據的排列順序
        # '-created'表明數據應該以倒序排列
        ordering = ('-created',)

    # 函數__str__定義當調用對象的str()方法時的返回值內容
    def __str__(self):
        # return self.title將文章標題返回
        return self.title

    # 獲取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    def was_created_recently(self):
        # 若文章是"最近"發表的，則返回True 
        diff = timezone.now() - self.created
        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            return True
        else:
            return False

