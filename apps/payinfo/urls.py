from django.urls import path
from . import views

app_name = 'payinfo'

urlpatterns = [
    path("",views.pay_index,name='payinfo')
]