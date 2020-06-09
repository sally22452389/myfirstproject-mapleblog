from django import forms
from django.contrib.auth.models import User
from .models import Profile

# 登錄表單，繼承了 forms.Form 適用於不與數據庫進行直接交互的功能
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

# 註冊表單，繼承forms.ModelForm
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 檢查兩次輸入密碼是否一致
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密碼輸入不一致，請重試。")

# 配置文件表單
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')