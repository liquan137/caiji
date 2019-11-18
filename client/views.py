from django.shortcuts import render, HttpResponse
from dwebsocket.decorators import accept_websocket


# Create your views here.

@accept_websocket
def path(request):
    if request.is_websocket():
        print(1)
        request.websocket.send('下载完成'.encode('utf-8'))
