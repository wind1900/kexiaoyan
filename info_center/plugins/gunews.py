# -*- coding: utf-8 -*-

from utils import *
from django.template import Template, Context
import requests
import re
import datetime

html = '''
<div class="cell"><a href="{{ more }}" target="_blank">研会新闻&gt;&gt;</a></div>
{% for link, name, time in news %}
<div class="smallcell bfont">
<a href="{{ link }}" target="_blank">{{ name }}</a> {{ time }}
</div>
{% endfor %}
'''

more = "http://gradunion.ustc.edu.cn"

def update():
    filename = get_filename(__name__)
    if need_update(filename):
        template = Template(html)
        c = Context({'more' : more})
        request = requests.get(more)
        content = request.content
        pattern = re.compile(r'<li><span class="time">(\d\d\d\d-)?(\d+?-\d+?)</span><a href="([\w_/.]+)">(.*?)</a></li>')
        l = pattern.findall(content)
        news = [(more + e[2][1:], e[3], parse_time(e[1], e[2])) for e in l]
        news.sort(key=lambda x:x[2], reverse=True)
        c['news'] = news[:10]
        content = template.render(c)
        f = open(filename, 'w')
        f.write(content.encode('utf8'))
        f.close()
    else:
        f = open(filename)
        content = f.read()
        f.close()
    return content

def parse_time(date, link):
    pattern = re.compile(r'[\w./_]*/(\d\d\d\d\d\d)/[\w./_]*')
    match = pattern.search(link).group(1)
    md = date.split('-')
    return datetime.date(int(match[:4]), int(md[0]), int(md[1])).strftime('%m-%d')
