from django.shortcuts import render
from .models import NewsCategory,News,Banner
from django.conf import settings
from .serializers import NewsSerializers,CommentSerializer
from django.http import Http404
from .forms import PublicCommentForm
from .models import Comment
from django.db.models import Q
from apps.xfzauth.decorators import xfz_login_required
# Create your views here.
from utils import restful
def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    #newses = News.objects.order_by('-pub_time')[0:count] #先在model中排序,再做切片操作
    #为了提高效率，降低数据库查找的次数,可提前把需要通过外键索引的字段查找出来
    newses = News.objects.select_related('category','author').all()[0:count]
    categories = NewsCategory.objects.all()
    #分类通过缓存当中去查找，效率会更高
    context = {
        'newses':newses,
        'categories':categories,
        'banners':Banner.objects.all()
    }
    return render(request,'news/index.html',context=context)

#处理新闻列表
def news_list(request):
    #通过p参数，来指定要获取第几页的数据
    #并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    page = int(request.GET.get('p',1))  #默认p=1
    #分类为0：代表不进行任何分来，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id',0)) #等于0不进行任何分类
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id ==0:
        newses = News.objects.select_related('category','author').all()[start:end]
    else:
        newses = News.objects.select_related('category','author').filter(category__id=category_id)[start:end]

    serializers = NewsSerializers(newses,many=True)#创建序列化
    data = serializers.data#通过serializers上的data属性拿到值
    return restful.result(data=data)


def news_detail(request,news_id):
    try:
        news = News.objects.select_related('category','author').prefetch_related('comments__author').get(pk=news_id)
        context={
            'news':news
        }
    except:
        raise Http404

    return render(request,'news/news_detail.html',context=context)

#发布评论的视图函数
@xfz_login_required  #后台限制
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment=Comment.objects.create(content=content,news=news,author=request.user)
        serializers = CommentSerializer(comment)
        data = serializers.data
        return restful.result(data=data)
    else:
        return restful.paramserror(message=form.get_errors())

def search(request):
    print('aaaaa')
    q = request.GET.get('q')  #拿到要查询的关键字q
    print(q)
    context = {}
    if q:  #或操作用Q表达式
        newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context['newses'] = newses
        print(newses)
    #根据q关键字在新闻中去取,将查询到的新闻返回
    return render(request, 'search/search.html', context=context)