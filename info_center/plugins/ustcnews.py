# -*- coding: utf-8 -*-

from utils import *
from django.template import Template, Context
import requests
import re

html = '''
科大要闻
{% for link, name, time in news %}
<div class="smallcell bfont">
<a href="{{ link }}" target="_blank">{{ name }}</a> {{ time }}
</div>
{% endfor %}
<div class="cell text-right"><a href="{{ more }}" target="_blank">更多...</a></div>
'''

more = "http://news.ustc.edu.cn"

def update():
    filename = get_filename(__name__)
    if need_update(filename):
        template = Template(html)
        c = Context({'more' : more})
        request = requests.get("http://www.ustc.edu.cn")
        content = request.content
        start = content.find('<TABLE width="100%">')
        end = content.find('</TABLE>', start)
        sc = content[start:end]
        match = []
        s = 0
        e = 0
        while True:
            s = sc.find('<a href="', e)
            if s < 0:
                break;
            e = sc.find('" target', s)
            link = sc[s+9:e]
            s = sc.find('blank">', e)
            e = sc.find('</a>', s)
            name = sc[s+7:e].replace('<br>', '')
            s = sc.find('size=1>', e)
            e = sc.find('</FONT>', s)
            date = sc[s+7:e].strip()
            match.append((link, name, date))
        c['news'] = match
        content = template.render(c)
        f = open(filename, 'w')
        f.write(content.encode('utf8'))
        f.close()
    else:
        f = open(filename)
        content = f.read()
        f.close()
    return content
