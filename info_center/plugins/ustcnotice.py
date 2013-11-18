# -*- coding: utf-8 -*-

from utils import *
from django.template import Template, Context
import requests
import re

html = '''
<div class="cell"><a href="{{ more }}" target="_blank">公告通知&gt;&gt;</a></div>
{% for link, name, time in notices %}
<div class="smallcell bfont">
<a href="{{ link }}" target="_blank">{{ name }}</a> {{ time }}
</div>
{% endfor %}
'''

more = "http://www.ustc.edu.cn/ggtz"

def update():
    filename = get_filename(__name__)
    if need_update(filename):
        template = Template(html)
        c = Context({'more' : more})
        request = requests.get("http://www.ustc.edu.cn")
        content = request.content
        start = content.find('<TABLE width="98%">')
        start = content.find('<TABLE width="98%">', start+19)
        end = content.find('</TABLE>', start)
        sc = content[start:end]
        match = []
        s = 0
        e = 0
        while True:
            s = sc.find('<a href="', e)
            if s < 0:
                break
            e = sc.find('">', s)
            link = "http://www.ustc.edu.cn" + sc[s+10:e]
            s = e + 2
            e = sc.find('</a>', s)
            name = sc[s:e]
            s = sc.find('size=1>', e)
            e = sc.find('</FONT>', s)
            date = sc[s+7:e]
            match.append((link, name, date))
        c['notices'] = match
        content = template.render(c)
        f = open(filename, 'w')
        f.write(content.encode('utf8'))
        f.close()
    else:
        f = open(filename)
        content = f.read()
        f.close()
    return content
