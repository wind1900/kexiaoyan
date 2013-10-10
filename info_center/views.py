from django.http import HttpResponse
from django.template import RequestContext, loader
import importlib
import models

def index(request):
    template = loader.get_template('index.html')
    material_list = models.Material.objects.all()
    context = RequestContext(request,
                             {'title':'hello~',
                              'material_list':material_list})
    return HttpResponse(template.render(context))

def fetion(request):
    template = loader.get_template('fetion.html')
    context = RequestContext(request,
                             {'title':'fetion'})
    return HttpResponse(template.render(context))

def update(request, source):
    try:
        module = importlib.import_module('info_center.plugins.'+source)
        return HttpResponse(module.update())
    except ImportError:
        return HttpResponse('404')

