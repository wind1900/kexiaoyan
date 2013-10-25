from django.template import Template, Context
import requests
import re

def update():
    s = __name__.rfind(".") + 1
    filename = __name__[s:]+".html"
    fp = open("info_center/plugins/" + filename)
    template = Template(fp.read())
    fp.close()
    c = Context({})
    c['huati'] = "abcde"
    session = requests.Session()
    session = requests.get('http://huati.weibo.com')
    rdata = session = requests.get('http://huati.weibo.com/aj_topiclist/small?_pv=1&ctg1=99&ctg2=0&prov=0&sort=time&p=1&t=1')
    element = r'<div class="hd"'
    return rdata
#    return template.render(c)
