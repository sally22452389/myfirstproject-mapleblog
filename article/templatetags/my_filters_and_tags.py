from django import template
from django.utils import timezone
import math

# 暫存
register = template.Library()

@register.filter(name='transfer')
def transfer(value, arg):
    """ 將輸出強制轉換為字符串 arg """
    return arg

@register.filter()
def lower(value):
    """ 將字符串轉換為小寫字符 """
    return value.lower()

# 獲取相對時間
@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '剛剛'

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分鐘前"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小時前"

    if diff.days >= 1 and diff.days < 30:
        return str(diff.days) + "天前"

    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + "個月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"

@register.inclusion_tag('article/tag_list.html')
def show_comments_pub_time(article):
    """顯示文章評論的發佈時間"""
    comments = article.comments.all()
    return {'comments': comments}