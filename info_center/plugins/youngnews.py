# -*- coding: utf-8 -*-

from utils import *
from django.template import Template, Context
import requests
import re
import datetime

html = '''
<div class="cell"><a href="{{ more }}" target="_blank">青春科大&gt;&gt;</a></div>
{% for link, name, time in news %}
<div class="smallcell bfont">
<a href="{{ link }}" target="_blank">{{ name }}</a> {{ time }}
</div>
{% endfor %}
'''

more = "http://young.ustc.edu.cn/"

def update():
    filename = get_filename(__name__)
    if need_update(filename):
        template = Template(html)
        c = Context({'more' : more})
        request = requests.get('http://young.ustc.edu.cn/firstlatest.php?reader=index')
        content = request.content.decode('gbk')
        pattern = re.compile(r'<a href="([\w?.=]+)" target="_blank"><font color=#00A4E8>(.*?)&nbsp;\[<font color=green>([\d/]+)</font>\]')
        l = pattern.findall(content)
        news = [(more + e[0], e[1], e[2].replace('/', '-')) for e in l[:10]]
        c['news'] = news
        content = template.render(c)
        f = open(filename, 'w')
        f.write(content.encode('utf8'))
        f.close()
    else:
        f = open(filename)
        content = f.read()
        f.close()
    return content
