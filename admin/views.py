from django.shortcuts import render
from django.http import HttpResponse
from admin.models import *
from current.models import *
import json
# Create your views here.

def test(request):
    search = m_contents_url.objects.get(url="https://www.ivsky.com/bizhi/bizhi/duckbill_boy_v41055/")
    return HttpResponse(search.id)

