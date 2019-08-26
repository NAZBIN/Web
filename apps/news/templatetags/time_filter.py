from datetime import datetime
from django import template
from django.utils.timezone import now as now_func
from django.utils.timezone import localtime

register = template.Library()  #创建模板库对象

def time_since(value):
    if isinstance(value,datetime):
        now = now_func()
        timestamp = (now - value).total_seconds()
        if timestamp<60:
            return "刚刚"
        elif timestamp>=60 and timestamp<=60*60:
            minutes = int(timestamp/60)
            return "{}分钟前".format(minutes)
        elif timestamp>60*60 and timestamp<=60*60*24:
            hours = int(timestamp/(60*60))
            return "{}小时前".format(hours)
        elif timestamp>60*60*24 and timestamp<=60*60*24*30:
            days = int(timestamp/(60*60*24))
            return "{}天前".format(days)
        else:
            return value.strftime("%Y/%m/%d %H:%M")
    else:
        return value

register.filter("time_since",time_since)


def time_format(value):
    if not isinstance(value, datetime):
        return value
    return localtime(value).strftime("%Y/%m/%d %H:%M:%S") #格式化当前时间

register.filter("time_format",time_format)