#coding:utf-8
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from models import *
import json
cursor = connection.cursor()
# Create your views here.

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def result(request):
    if request.method == 'GET':
        return HttpResponse(status=400, content=u'请求方法类型错误')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    if username and password and email:
        if not User.objects.filter(name=username).exists():
            User.objects.create(name=username, password=password, email=email)
        else:
            return HttpResponse(status=200, content=u'用户已存在')
    else:
        return HttpResponse(status=200, content=u'缺少必填参数')
    flag = 0
    data = {'flag': flag}
    return render(request, 'result.html', {'data': json.dumps(data)})

def search_user(request):
    flag = False
    name = request.GET.get('username', None)
    if name:
        if User.objects.filter(name=name).exists():
            flag = True
    return JsonResponse({'flag': flag})

def user_login(request):
    flag = False
    name = request.GET.get('username', None)
    password = request.GET.get('password', None)
    if name and password:
        cursor = connection.cursor()
        # 1' OR '1'='1
        strSQL = "SELECT * FROM index_user WHERE (name = '" + name + "') and (password = '" + password + "');"
        cursor.execute(strSQL)
        all = cursor.fetchall()
        if all:
            flag = True
            res = JsonResponse({'flag': flag, 'users': all})
            try:
                id = User.objects.get(name=name).id
                res.set_cookie('user_id', id)
            except:
                pass
            return res
    return JsonResponse({'flag': flag, 'users': all})

def show(request):
    id = request.COOKIES.get('user_id')
    if id:
        name = User.objects.filter(id=id).first().name
        return render(request, 'show.html', {'name': name})
    else:
        return HttpResponseRedirect('/event/index/login/')
        # return render(request, 'login.html')

def searchbyname(request):
    name = request.GET.get('username', None)
    result = {}
    if name:
        users = User.objects.filter(name__startswith=name)
    else:
        users = User.objects.all()
    for u in users:
        result[u.id] = [u.name, u.email]
    return HttpResponse(content_type='application/json', content=json.dumps(result, ensure_ascii=False))