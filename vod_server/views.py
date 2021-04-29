import os
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + '\\..\\'

def MainPage(request):
    return render(request, 'Home.html')

def DefaultPage(request):
    return HttpResponse('这是后端，请从前端访问' + '127.0.0.1:8080')

def upload(request):
    file = request.FILES.get('file')
    url = os.path.join(BASE_DIR, 'static/Upload_File', file.name)
    res = file.file
    f = open(url, 'wb')
    for chunk in file.chunks():
        f.write(chunk)
    # f.write(file.read())
    f.close()
    jsondata = json.dumps({"code": 200, "msg": {"url": 'static/Upload_File/%s' % (file.name), 'filename': file.name}})
    return HttpResponse(jsondata, content_type="application/json")

def GetFileName(request):
    aList = os.listdir(os.path.join(BASE_DIR, 'static/Upload_File'))
    bList = os.listdir(os.path.join(BASE_DIR, 'static/Processed_File'))
    jsondata = json.dumps({"code": 200, "msg": {"RowFileNameList": aList, "ProcessedFileNameList": bList}})
    return HttpResponse(jsondata, content_type="application/json")
