from django.shortcuts import render
from .models import Course,CourseCategory,CourseOrder
from utils import restful
from django.conf import settings
from apps.xfzauth.decorators import xfz_login_required
from hashlib import md5
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt
import time,hmac,os,hashlib
def course_index(request):
    context = {
        'courses':Course.objects.all()
    }
    return render(request,'course/course_index.html',context=context)

def course_detail(request,course_id):
    course = Course.objects.get(pk=course_id)
    #这里最好用try except来捕获异常
    context = {
        'course':course
    }
    return render(request,'course/course_detail.html',context=context)

def course_token(request):
    # video：是视频文件的完整链接
    file = request.GET.get('video')

    course_id = request.GET.get('course_id')
    if not CourseOrder.objects.filter(course_id=course_id,buyer=request.user,status=2).exists():
        return restful.paramserror(message='请先购买课程！')

    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})

#限制登录状态下才能进行   (课程订单)
@xfz_login_required
def course_order(request,course_id):
    course = Course.objects.get(pk=course_id)
    order = CourseOrder.objects.create(course=course,buyer=request.user,status=1,amount=course.price)
    context = {
        'goods': {
            'thumbnail': course.cover_url,
            'title': course.title,
            'price': course.price
        },
        'order': order,
        # /course/notify_url/
        'notify_url': request.build_absolute_uri(reverse('course:notify_view')),
        'return_url': request.build_absolute_uri(reverse('course:course_detail',kwargs={"course_id":course.pk}))
    }
    return render(request,'course/course_order.html',context=context)

@xfz_login_required
def course_order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")

    token = 'f083578bddcdbb3e490ba68ed92bfe88'
    uid = '09f18adb4f85817cab298f48'
    orderuid = str(request.user.pk)

    print('goodsname:',goodsname)
    print('istype:',istype)
    print('notify_url:',notify_url)
    print('orderid:',orderid)
    print('price:',price)
    print('return_url:',return_url)

    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()
    return restful.result(data={"key": key})


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    print('='*10)
    print(orderid)
    print('='*10)
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()

