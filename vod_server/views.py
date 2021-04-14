from django.shortcuts import render
from django.http import HttpResponse
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__)) +'\\..\\'

def MainPage(request):

    return render(request,'Home.html')

def upload(request):
    if request.method == 'POST':# 获取对象
        obj = request.FILES.get('Get_Files')
        # 上传文件的文件名 　　　　
        print(obj.name)        
        f = open(os.path.join(BASE_DIR ,'Upload_File', obj.name), 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        return  HttpResponse('OK')
    return HttpResponse('Error')

def DefaultPage(request):

    return HttpResponse('这是后端，请从前端访问'+ '127.0.0.1:8080')