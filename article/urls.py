from django.urls import path
from . import views


app_name = 'article' # 部署應用名

urlpatterns = [
    path('article-list/', views.article_list, name='article_list'), 
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'), # 文章詳情 傳遞id函數到視圖
    path('article-create/', views.article_create, name='article_create'), # 發表文章
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'), #刪除文章
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'), # 安全刪除文章
    path('article-update/<int:id>/', views.article_update, name='article_update'), # 更新文章
    path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'), # 點讚
]






