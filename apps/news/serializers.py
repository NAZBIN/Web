#专门用来管理序列化，使用的是DRF   (Django Rest framework)
#根据模型直接序列化

from rest_framework import serializers
from .models import News,NewsCategory,Comment,Banner
from apps.xfzauth.serializers import UserSerializers
class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')

class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializers() #把它序列化 以后拿到这个category会包含id和name
    author = UserSerializers()
    class Meta:
        model = News
        fields = ('id','title','desc','category','thumbnail','pub_time','author')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','content','author','pub_time')

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id','image_url','priority','link_to')

