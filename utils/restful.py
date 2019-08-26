#encoding: utf-8
from django.http import JsonResponse

class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500

# {"code":400,"message":"","data":{}}
def result(code=HttpCode.ok,message="",data=None,kwargs=None):
    json_dict = {"code":code,"message":message,"data":data}

    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def ok():
    return result()


def paramserror(message="",data=None):
    return result(code=HttpCode.paramserror,message=message,data=data)

def unauth(message="",data=None):
    return result(code=HttpCode.unauth,message=message,data=data)

def methoderror(message='',data=None):
    return result(code=HttpCode.methoderror,message=message,data=data)

def servererror(message='',data=None):
    return result(code=HttpCode.servererror,message=message,data=data)

