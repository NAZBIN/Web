#encoding:utf-8

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import  models

#重新定义manager对象
class UserManager(BaseUserManager):
    #下划线表示受保护的方法，不能在外部使用
    def _create_user(self,telephone,username,password,**kwargs):
        if not telephone:
            raise ValueError("请输入手机号码!")
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")

        user = self.model(telephone=telephone,username=username,**kwargs)    #代表当前的user
        user.set_password(password)
        user.save()
        return user
    #创建普通用户
    def create_user(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone,username,password,**kwargs)

    #创建超级用户
    def create_superuser(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone,username,password,**kwargs)





class User(AbstractBaseUser,PermissionsMixin):
    # 创建主键
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11,unique=True)
    email = models.EmailField(unique=True,null=True)
    username = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username