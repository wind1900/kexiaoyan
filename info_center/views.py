# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt
import plugins.weather
import importlib
import models
import datetime
import lunardate
import random

fetion_template = '''小研播报：
【天气】{{weather}}
【要闻】
【通知】
【回顾】
【征集\招募】
【预告】
{{birthday}}(小研心情)
今天的科小研播报就到这里，我们明天再会{{emotion}}
'''

def index(request):
    template = loader.get_template('index.html')
    material_list = models.Material.objects.all()
    context = RequestContext(request,
                             {'title':'hello~',
                              'material_list':material_list,
                              'active_navbar':'index',
                              'span': (8, 4)})
    return HttpResponse(template.render(context))

def fetion(request):
    today = datetime.date.today()
    todaya1 = today + datetime.timedelta(days=1)
    todaya7 = today + datetime.timedelta(days=7)
    todayb7 = today - datetime.timedelta(days=7)
    todayb1 = today - datetime.timedelta(days=1)
    todayb2 = today - datetime.timedelta(days=2)
    future = models.Event.objects.filter(date__gt=todaya1, 
                                         date__lte=todaya7)
    tomorrow = models.Event.objects.filter(date=todaya1)
    now = models.Event.objects.filter(date = today)
    past = models.Event.objects.filter(date__gte=todayb7,
                                       date__lt=today)
    lunar_today = lunardate.LunarDate.fromSolarDate(today.year, today.month, today.day)
    lunar_todaya1 = lunardate.LunarDate.fromSolarDate(todaya1.year, todaya1.month, todaya1.day)

    mthn = 100 * ((today.day-1)//7 + 1) + today.weekday() + 1
    mthn1 = 100 * ((todaya1.day-1)//7 + 1) + todaya1.weekday() + 1
    memdays = models.Memday.objects.filter(Q(month=today.month, day = today.day, lunar = False) | Q(month = lunar_today.month, day = lunar_today.day, lunar = True) | Q(month = today.month, day = mthn, lunar = False))
    tomorrow_memdays = models.Memday.objects.filter(Q(month=todaya1.month, day = todaya1.day, lunar = False) | Q(month = lunar_todaya1.month, day = lunar_todaya1.day, lunar=True) | Q(month = today.month, day = mthn1, lunar = False))
    memdays = " ".join(e.name for e in memdays)
    tomorrow_memdays = " ".join(e.name for e in tomorrow_memdays)

    try:
        fetionb1 = models.FetionText.objects.get(date = todayb1)
    except ObjectDoesNotExist:
        fetionb1 = models.FetionText(content="无")
    try:
        fetionb2 = models.FetionText.objects.get(date = todayb2)
    except ObjectDoesNotExist:
        fetionb2 = models.FetionText(content="无")
    try:
        fetion = models.FetionText.objects.get(date = today)
    except ObjectDoesNotExist:
        fetion = None

    if fetion and len(fetion.content) > 20:
        fetion_today = fetion.content
    else:
        weather = plugins.weather.update()
        birthday = []
        emotion = ('~(@^_^@)~', '~~o(^_^)o~~', '~O(∩_∩)O~', '~\(≧▽≦)/~', '~(*^__^*)~')
        today_birthday = models.Birthday.objects.filter(
            Q(month=today.month, day=today.day, lunar=False) | 
            Q(month=lunar_today.month, day=lunar_today.day, 
              lunar=True))
        tomorrow_birthday = models.Birthday.objects.filter(
            Q(month=todaya1.month, day=todaya1.day, lunar=False) | 
            Q(month=lunar_todaya1.month,
              day=lunar_todaya1.day, lunar=True))
        if today_birthday:
            tbtext = u', '.join(b.name + '(' + b.phone + ')' for b in today_birthday)
            birthday.append(u'今天是' + tbtext + u'的生日')
        if tomorrow_birthday:
            tbtext = u', '.join(b.name + '(' + b.phone + ')' for b in tomorrow_birthday)
            birthday.append(u'明天是' + tbtext + u'的生日')
        birthday = u'，'.join(birthday)
        if birthday:
            birthday = u'【生日】' + birthday + u'，大家快去送上祝福吧~\n'
        fetion_today = Template(fetion_template).render(
            Context({'weather':weather,
                     'birthday':birthday,
                     'emotion':random.choice(emotion)}))
    template = loader.get_template('fetion.html')
    context = RequestContext(request,
                             {'title':'fetion',
                              'active_navbar':'fetion',
                              'span' : (6, 6),
                              'future':future,
                              'tomorrow':tomorrow,
                              'now':now,
                              'past':past,
                              'now_memdays':memdays,
                              'tomorrow_memdays':tomorrow_memdays,
                              'fetionb1':fetionb1,
                              'fetionb2':fetionb2,
                              'fetion':fetion_today,})
    return HttpResponse(template.render(context))

@csrf_exempt
def submit_fetion(request):
    content = request.POST['content']
    date = datetime.date.today()
    try:
        fetion = models.FetionText.objects.get(date = date)
    except ObjectDoesNotExist:
        fetion = models.FetionText(date=date)
    fetion.content = content
    fetion.save()
    return HttpResponse('ok')

def update(request, source):
    try:
        module = importlib.import_module('info_center.plugins.'+source)
        return HttpResponse(module.update())
    except ImportError:
        return HttpResponse('404')

