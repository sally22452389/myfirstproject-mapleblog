from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from article.models import ArticlePost

# Create your views here.

class CommentNoticeListView(LoginRequiredMixin, ListView):
    """
    通知列表
    unread()方法是django-notifications
    """
    # 上下文的名稱
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/list.html'
    # 登錄重定向
    login_url = '/userprofile/login/'

    # 未讀通知查詢
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
    """
    更新通知狀態
    """
    # 處理get請求
    def get(self, request):
        # 獲取未讀消息
        notice_id = request.GET.get('notice_id')
        # 更新單條通知
        if notice_id:
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')