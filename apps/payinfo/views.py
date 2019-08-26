from django.shortcuts import render

def pay_index(request):
    return render(request,'payinfo/payinfo.html')