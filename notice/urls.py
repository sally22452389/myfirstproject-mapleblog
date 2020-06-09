from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    path('list/', views.CommentNoticeListView.as_view(), name='list'), # 通知列表
    path('update/', views.CommentNoticeUpdateView.as_view(), name='update'), # 通知更新
]