from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment

from notifications.signals import notify
from django.contrib.auth.models import User

# Create your views here.

# 文章評論
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 處理POST請求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        # 新回覆
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            # 二次回覆
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回覆層級超過二級，則轉換為二級
                new_comment.parent_id = parent_comment.get_root().id
                # 被回覆人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                # 給其他用戶通知發送
                if not parent_comment.user.is_superuser and not parent_comment.user == request.user:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user, # 接收者
                        verb='回覆了你', # 動詞
                        target=article, # 目標對象
                        action_object=new_comment, # 動作物件
                    )
                
                # return HttpResponse("200 OK")
                return JsonResponse({"code": "200 OK", "new_comment_id": new_comment.id})

            new_comment.save()

            # 給管理員通知發送
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回覆了你',
                    target=article,
                    action_object=new_comment,
                )
            # 錨點
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            return redirect(redirect_url)
        else:
            return HttpResponse("內容有誤，請重新填寫。")
    # GET 
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse("發表評論僅接受POST請求。")