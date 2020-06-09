from django.shortcuts import render
from django.http import HttpResponse
from .models import ArticlePost, ArticleColumn #文章發布, 欄目
import markdown
from django.shortcuts import render, redirect, get_object_or_404 # 重導向重定向
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator # 分頁模塊
from django.db.models import Q # 對象
from comment.models import Comment
from comment.forms import CommentForm

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

# Create your views here.


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    # 初始化查詢
    article_list = ArticlePost.objects.all()
    # 搜索查询
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 欄目查詢
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 標籤查詢
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查詢排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')


    # articles = ArticlePost.objects.all() # 獲得所有文章
    # 根據GET請求中查詢條件
    # 返回不同排序順序的對像數組
    # if request.GET.get('order') == 'total_views': 
    #     article_list = ArticlePost.objects.all().order_by('-total_views')
    #     order = 'total_views'
    # else:
    #     article_list = ArticlePost.objects.all()
    #     order = 'normal'

    paginator = Paginator(article_list, 3) # 每頁顯示X篇文章
    page = request.GET.get('page') # 獲取url中的頁碼
    articles = paginator.get_page(page) # 將導航對象相應的頁碼內容返回給articles 

    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    } # 傳遞給模板，每頁的文章、排序、搜索、欄目、標籤

    return render(request, 'article/list.html', context) # render函數:載入模板，返回context對象


# 文章詳情
def article_detail(request, id):
    # article = ArticlePost.objects.get(id=id) # 取出id相應一篇文章
    article = get_object_or_404(ArticlePost, id=id)
    comments = Comment.objects.filter(article=id) # 取出文章評論

    # 瀏覽量
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 將markdown語法渲染成html樣式
    md = markdown.Markdown( 
        extensions = [
        'markdown.extensions.extra', # 縮寫、表格等
        'markdown.extensions.codehilite', # code高亮度圖像
        'markdown.extensions.toc', # 目錄功能
        ]
    )    
    article.body = md.convert(article.body)
    comment_form = CommentForm()
    context = { 
        'article': article, 
        'toc': md.toc, 
        'comments': comments,
        'comment_form': comment_form,
        } # 傳遞給模板顯示文章、目錄、評論、表單

    return render(request, 'article/detail.html', context)

# 寫文章視圖
@login_required(login_url='/userprofile/login/') # 必須登入
def article_create(request):
    if request.method == "POST": # 判斷是否提交數據
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        article_post_form = ArticlePostForm(request.POST) # 將提交的數據賦值到表單
        if article_post_form.is_valid(): # 判斷提交的數據是否滿足模型的要求
            new_article = article_post_form.save(commit=False) # 保存數據，但暫時不提交到資料庫中
            # 指定數據庫中id=1的用戶為作者
            # 如果你進行過刪除數據表的操作，可能會找不到id=1的用戶
            # 此時請重新創建用戶，並傳入此用戶的id 
            # new_article.author = User.objects.get(id=1)
            # 指定目前登錄的用戶為作者
            new_article.author = User.objects.get(id=request.user.id)
            # 判斷是否設定欄目
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            new_article.save() # 將新文章保存到資料庫中
            # 保存 tags 的多對多關係
            article_post_form.save_m2m()
            return redirect("article:article_list") 
        else: 
            return HttpResponse("內容有誤，請重新填寫。") # 如果數據不合，返回錯誤
    else: # 如果請求獲取數據
        article_post_form = ArticlePostForm() # 創建表單
        columns = ArticleColumn.objects.all()
        context = { 'article_post_form': article_post_form, 'columns': columns }
        return render(request, 'article/create.html', context)

# 刪除文章
@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    article = ArticlePost.objects.get(id=id) # 根據id獲取需要刪除的文章

    if request.user != article.author: # 如果需求user非文章作者
        return HttpResponse("抱歉，你無權刪除這篇文章。")

    article.delete()
    return redirect("article:article_list")

# 安全刪除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)

        if request.user != article.author: # 如果需求user非文章作者
            return HttpResponse("抱歉，你無權刪除這篇文章。")

        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("僅允許post請求")

# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的視圖函數
    通過POST方法提交表單，更新title、body字段
    GET方法進入初始表單頁面
    id：文章的id 
    """
    # 獲取需要修改的文章對象
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author: # 如果需求user非文章作者
        return HttpResponse("抱歉，你無權修改這篇文章。")

    # 判斷用戶是否為POST提交表單數據
    if request.method == "POST":
        # 將提交的數據賦值到表單實例中
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            # 保存新寫入的title、body數據並保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            # 判斷是否設定欄目
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            # 標題圖屬文件 request.FILES 獲取
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            # tags 非一般字段 tags.set() / tags.names() , 數據更新/獲取標籤名
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            
            article.save()

            # 完成後返回到修改後的文章中。需傳入文章的id
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("內容有誤，請重新填寫。")

    # 如果用戶GET請求獲取數據
    else:
        article_post_form = ArticlePostForm()
        # 賦值上下文，將article文章對像也傳遞進去，以提取舊的內容
        columns = ArticleColumn.objects.all()
        context = { 
            'article': article, 
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        return render(request, 'article/update.html', context)

# 點讚
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')
