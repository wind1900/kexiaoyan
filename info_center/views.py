from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q
import importlib
import models
import datetime
import lunardate

def index(request):
    template = loader.get_template('index.html')
    material_list = models.Material.objects.all()
    context = RequestContext(request,
                             {'title':'hello~',
                              'material_list':material_list,
                              'active_navbar':'index'})
    return HttpResponse(template.render(context))

def fetion(request):
    today = datetime.date.today()
    todaya1 = today + datetime.timedelta(days=1)
    todaya7 = today + datetime.timedelta(days=7)
    todayb7 = today - datetime.timedelta(days=7)
    future = models.Event.objects.filter(date__gt=todaya1, 
                                         date__lte=todaya7)
    tomorrow = models.Event.objects.filter(date=todaya1)
    now = models.Event.objects.filter(date = today)
    past = models.Event.objects.filter(date__gte=todayb7,
                                       date__lt=today)
    lunar_today = lunardate.LunarDate.fromSolarDate(today.year, today.month, today.day)
    lunar_todaya1 = lunardate.LunarDate.fromSolarDate(todaya1.year, todaya1.month, todaya1.day)
    mthn = 100 * (today.day//7 + 1) + today.weekday() + 1
    mthn1 = 100 * (todaya1.day//7 + 1) + todaya1.weekday() + 1
    memdays = models.Memday.objects.filter(Q(month=today.month, day = today.day, lunar = False) | Q(month = lunar_today.month, day = lunar_today.day, lunar = True) | Q(month = today.month, day = mthn, lunar = False))
    tomorrow_memdays = models.Memday.objects.filter(Q(month=todaya1.month, day = todaya1.day, lunar = False) | Q(month = lunar_todaya1.month, day = lunar_todaya1.day, lunar=True) | Q(month = today.month, day = mthn1, lunar = False))
    memdays = " ".join(e.name for e in memdays)
    tomorrow_memdays = " ".join(e.name for e in tomorrow_memdays)
    template = loader.get_template('fetion.html')
    context = RequestContext(request,
                             {'title':'fetion',
                              'active_navbar':'fetion',
                              'future':future,
                              'tomorrow':tomorrow,
                              'now':now,
                              'past':past,
                              'now_memdays':memdays,
                              'tomorrow_memdays':tomorrow_memdays})
    return HttpResponse(template.render(context))

def update(request, source):
    try:
        module = importlib.import_module('info_center.plugins.'+source)
        return HttpResponse(module.update())
    except ImportError:
        return HttpResponse('404')

