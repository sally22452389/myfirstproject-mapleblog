from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver # 接收器

# Create your models here.

# 用戶資料擴展
class Profile(models.Model):
    # 與User模型構成一對一的關係
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True) # %Y%m%d日期格式化
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


# 信號接收函數，每當新建User實例時自動調用 objects物件 instance實例 sender發送者
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# 信號接收函數，每當新建User實例時自動調用
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
