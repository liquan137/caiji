from django.shortcuts import render
from django.http import HttpResponse
from admin.models import *
from current.models import *
# Create your views here.

def test(request):
    try:
        father = m_f_project(title='淘宝素材')
        father.save()
        return HttpResponse('创建成功')
    except:
        return HttpResponse('无法重复创建')

