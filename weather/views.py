#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.decorators import api_view
import json
import time

@api_view(['POST'],)
def getWeather(request):
    result = {}
    if request.method == 'POST':
        if 'application/json' not in request.META['CONTENT_TYPE']:
            return HttpResponse(status=400, content=u'请求格式无效')
        try:
            req = json.loads(request.body)
        except:
            result['error_code'] = 10003
            return HttpResponse(content_type='application/json', content=json.dumps(result, ensure_ascii=False))

        city_code = req.get('theCityCode')
        if city_code:
            date = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
            if city_code == 1:
                cid = '01'
                name = u'北京'
                weather_info = u'今日天气实况：气温：19℃；风向/风力：东北风 1级；湿度：54%'
                error_code = 0
            elif city_code == 2:
                cid = '02'
                name = u'上海'
                weather_info = u'今日天气实况：气温：25℃；风向/风力：北风 2级；湿度：70%'
                error_code = 0
            else:
                result['error_code'] = 10002
                return HttpResponse(content_type='application/json', content=json.dumps(result, ensure_ascii=False))
        else:
            result['error_code'] = 10001
            return HttpResponse(content_type='application/json', content=json.dumps(result, ensure_ascii=False))
    else:
        return HttpResponse(status=400, content=u'请求类型错误')
    result['cid'] = cid
    result['name'] = name
    result['weather_info'] = weather_info
    result['date'] = date
    result['error_code'] = 0
    return HttpResponse(content_type='application/json', content=json.dumps(result, ensure_ascii=False))