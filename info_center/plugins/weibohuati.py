# -*- coding: utf-8 -*-

from django.template import Template, Context
from utils import *
import requests
import re

html = '''
{% for link, name in huati %}
<div class="cell text-right">
<a href="{{ link }}" target="_blank">{{ name }}</a>
</div>
{% endfor %}
<div class="cell text-right"><a href="{{ more }}" target="_blank">更多热门话题</a></div>
'''

more = "http://huati.weibo.com"

def update():
    filename = get_filename(__name__)
    if need_update(filename):
        template = Template(html)
        c = Context({'more': more})
        request = requests.get("http://huati.weibo.cn")
        content = request.content
        pattern = re.compile(ur'<a href="([\w:/?=.]+)" class="k">(#[\w,，+“”、\-——《》<>!]+#)</a>', re.UNICODE)
        match = pattern.findall(request.content.decode('utf8'))
        c['huati'] = match[:10]
        content = template.render(c)
        f = open(filename, 'w')
        f.write(content.encode('utf8'))
        f.close()
    else:
        f = open(filename)
        content = f.read()
        f.close()
    return content
