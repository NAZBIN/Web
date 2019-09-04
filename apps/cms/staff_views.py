from django.shortcuts import render,redirect,reverse
from apps.xfzauth.models import User
from django.contrib.auth.models import Group
from django.views.generic import View
from utils import restful
from apps.xfzauth.decorators import xfz_superuser_required
from django.utils.decorators import method_decorator
@xfz_superuser_required
def staff_view(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs':staffs
    }
    return render(request,'cms/staffs.html',context=context)

@method_decorator(xfz_superuser_required,name='dispatch')  #装饰到类视图的dispatch上面
class add_staff_view(View):
    def get(self,request):
        groups = Group.objects.all()
        context = {
            'groups': groups
        }
        return render(request, 'cms/add_staff.html', context=context)
    def post(self,request):
        telephone = request.POST.get('telephone')
        if not User.objects.filter(telephone=telephone).exists():
            return restful.paramserror(message='该员工不存在')
        user =User.objects.filter(telephone=telephone).first()  #根据电话号取到用户
        #如果用户存在,把该用户设置成管理员
        user.is_staff = True
        #拿到前端所有用户勾选的分组
        group_ids = request.POST.getlist("groups")  #拿到所有分组的id
        groups = Group.objects.filter(pk__in=group_ids)
        #注意：用户和分组时多对多的关系，如果将用户和分组绑定起来
        user.groups.set(groups)
        user.save()
        #user上面有一个group属性，group是多对多的关系 通过set把它设置进去
        return redirect(reverse('cms:staffs'))