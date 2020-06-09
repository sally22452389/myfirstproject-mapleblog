from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required # 驗證登錄裝飾器
from .models import Profile

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data清理出合法數據
            data = user_login_form.cleaned_data
            # 檢驗賬號、密碼是否正確匹配數據庫中的某個用戶
            # 如果均匹配則返回這個user
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 將用戶數據保存在session會話中，即實現了登錄動作
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse("帳號或密碼輸入錯誤。請重新輸入。")
        else:
            return HttpResponse("帳號或密碼輸入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("請使用GET或POST請求數據")


def user_logout(request):
    logout(request)
    return redirect("article:article_list")

# 註冊
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 設置密碼
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 存好數據後立即登錄並返回列表
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("輸入有誤。請重新輸入")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("請使用GET或POST請求數據")

@login_required(login_url='/userprofile/login/') # 必須登入
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 驗證登錄用戶、待刪除用戶是否相同
        if request.user == user:
            # 登出，刪除數據並返回
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("你沒有操作刪除的權限。")
    else:
        return HttpResponse("僅接受post請求。")

# 編輯用戶資料
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id是OneToOneField自動生成的字段
    # profile = Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 驗證修改數據者，是否為用戶本人
        if request.user != user:
            return HttpResponse("你沒有權限修改此用戶訊息。")

        # profile_form = ProfileForm(data=request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗後的合法數據cleaned_data
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            # 如果request.FILES存在文件，則保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            # 帶參數的重定向redirect() 
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("註冊表單輸入有誤。請重新輸入")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("請使用GET或POST請求數據")
