from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {'title':'hello~'})
    return HttpResponse(template.render(context))

def fetion(request):
    template = loader.get_template('fetion.html')
    context = RequestContext(request, {'title':'fetion'})
    return HttpResponse(template.render(context))
