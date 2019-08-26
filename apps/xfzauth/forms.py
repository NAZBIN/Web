from django import  forms
from apps.forms import  FormMixin
from django.core.cache import cache
from .models import User
#表单代码
class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=10,min_length=6,error_messages={"max_length":"密码不能超过10位",
                                                                          "min_length":"密码不能少于6个字符"})
    remember = forms.IntegerField(required=False)

    #get_errors 来提取错误信息

class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=10,min_length=6,error_messages={"max_length":"密码不能超过10位",
                                                                          "min_length":"密码不能少于6个字符"})
    password2 = forms.CharField(max_length=10,min_length=6,error_messages={"max_length":"密码不能超过10位",
                                                                          "min_length":"密码不能少于6个字符"})
    img_captcha = forms.CharField(min_length=4,max_length=4)
    sms_captcha = forms.CharField(min_length=4,max_length=4)
    #验证密码1和密码2是否相等
    #重写clean方法
    def clean(self):
        cleaned_date = super(RegisterForm, self).clean()
        #从cleaned_date中取数据
        telephone = cleaned_date.get('telephone')
        password1 = cleaned_date.get('password1')
        password2 = cleaned_date.get('password2')
        if password1 != password2:
            raise forms.ValidationError("两次输入密码不一致！")
        #验证手机号是否存在
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError("手机号已经被注册！")
        #验证img和sms是否在缓存中
        img_captcha = cleaned_date.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha.lower())
        if not cached_img_captcha or cached_img_captcha.lower()!=img_captcha.lower():
            raise forms.ValidationError("图形验证码错误！")

        cached_sms_captcha = cache.get(telephone)
        sms_captcha = cleaned_date.get('sms_captcha')
        if not cached_sms_captcha or cached_sms_captcha.lower()!=sms_captcha.lower():
            raise forms.ValidationError("手机验证码错误")
