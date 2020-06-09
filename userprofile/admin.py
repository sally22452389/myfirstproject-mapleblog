from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.

# 定義一個行內admin 
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'

# 將Profile關聯到User中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# 重新註冊User 
admin.site.unregister(User)
admin.site.register(User, UserAdmin)