#encoding: utf-8

from haystack import indexes
from .models import News
#构建索引类，使用搜索引擎
class NewsIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return News   #指定索引是为哪个模板服务的

    def index_queryset(self, using=None):  #代表以后从news中提取数据的时候要返回什么样的值
        return self.get_model().objects.all() #全部返回