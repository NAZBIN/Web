from django.db import models
from shortuuidfield import ShortUUIDField

class Course(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey('CourseCategory',on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher',on_delete=models.DO_NOTHING)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField()
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)

class CourseCategory(models.Model):
    name = models.CharField(max_length=100)


class Teacher(models.Model):
    username = models.CharField(max_length=100)
    avatar = models.URLField()
    jobtitle = models.CharField(max_length=100)
    profile = models.TextField()

#课程与分类是一对一的关系， 分类与课程是多对一的关系
#课程与讲师是多对一的关系


class CourseOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    course = models.ForeignKey("Course",on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey("xfzauth.User",on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1：代表的是支付宝支付。2：代表的是微信支付
    istype = models.SmallIntegerField(default=0)
    # 1：代表的是未支付。2：代表的是支付成功
    status = models.SmallIntegerField(default=1)