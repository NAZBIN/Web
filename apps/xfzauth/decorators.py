from utils import restful
from django.shortcuts import redirect
from functools import wraps
from django.http import Http404
def xfz_login_required(func): #装饰器第一个参数，接受一个函数
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated: #已经授权说明已经登陆
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录!')
            else:
                #如果不是ajax请求那么进行重定向
                return redirect('/')

    return wrapper

def xfz_superuser_required(viewfunc):
    @wraps(viewfunc)
    def decorator(request,*args,**kwargs):
        if request.user.is_superuser:
            return viewfunc(request,*args,**kwargs)
        else:
            raise Http404

    return decorator
