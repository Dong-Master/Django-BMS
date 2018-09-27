#coding:utf-8
#@mail:879995812@qq.com

from django.shortcuts import render

def base(request):

    return render(request,'base.html')