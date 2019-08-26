from django.contrib.auth import  login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from utils import restful
from django.shortcuts import redirect,reverse
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from django.http import HttpResponse
from django.core.cache import cache
from utils import smssender
from django.contrib.auth import get_user_model

User = get_user_model()
# 处理前端post请求
@require_POST
def login_view(request):
    #需要一个表单对数据进行验证
    #导入表单使用表单做验证
    form = LoginForm(request.POST)
    if form.is_valid():
        #如果验证成功，拿到数据
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username = telephone,password=password)
        if user:
            #验证成功后判断 is_active看该用户是否可用
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message="您的账号已经被冻结")
        else:
            return restful.paramserror(message="手机号码或者密码错误")
    else:
        errors = form.get_errors()
        return restful.paramserror(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

@require_POST
def register(request):
    #写验证表单
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        #存储到数据库
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request,user)
        #告诉前端我已登录成功
        return restful.ok()
    else:
        return restful.paramserror(message=form.get_errors())

#图形验证码视图函数
def img_captcha(request):
    #产生文本和图片
    text,image = Captcha.gene_code()
    out = BytesIO()  #创建一个流对象
    image.save(out,'png')
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    response.write(out.read())

    response['Content-length'] = out.tell()
    #把验证码存储在缓存系统中
    cache.set(text.lower(),text.lower(),5*60) #过期时间五分钟
    #把小写验证码作为key并把这个value存储起来

    return response

# def sms_captcha(request):
#     telephone = request.GET.get('telephone')
#     code = Captcha.gene_text()
#     cache.set(telephone,code,5*60)
#     result = smssender.send(telephone,code)
#     if result:
#         print('短信验证码:', code)
#         return restful.ok()
#     else:
#         return restful.paramserror(message="短信验证码发送失败！")

    #测试用
def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    cache.set(telephone,code,5*60)
    print('短信验证码:', code)
    return restful.ok()


#测试cache 把数据保存在memcached中，然后立即读取
def cache_test(request):
    cache.set('username','zhiliao',60)
    result = cache.get('username')
    print(result)
    return HttpResponse('success')