# -*- coding: utf-8 -*-

from utils import *
from django.template import Template, Context
import requests
import re
import datetime
import HTMLParser

html = '''
<div class="cell"><a href="{{ more }}" target="_blank">bbs通知&gt;&gt;</a></div>
{% for link, name, time in notices %}
<div class="smallcell bfont">
<a href="{{ link }}" target="_blank">{{ name }}</a> {{ time }}
</div>
{% endfor %}
'''

more = "http://bbs.ustc.edu.cn/cgi/bbsdoc?board=Notice"

def update():
    filename = get_filename(__name__)
    if need_update(filename):
        template = Template(html)
        c = Context({'more' : more})
        request = requests.get(more)
        content = request.content.decode('gb2312')
        pattern = re.compile(ur'<tr class="new">.+?</tr>', re.U | re.S)
        notices = pattern.findall(content)
        parser = HTMLParser.HTMLParser()
        match = []
        for notice in notices[:10]:
            s = notice.find('datetime"')
            e = notice.find('</td>', s)
            date = notice[s+10:e]
            date = datetime.datetime.strptime(date, '%a %b %d')
            date = date.strftime('%m-%d')
            s = notice.find('o_title" href="', e)
            e = notice.find('">', s)
            link = parser.unescape("http://bbs.ustc.edu.cn/cgi/" + notice[s+15:e])
            s = e+2
            e = notice.find('</a>', s)
            name = parser.unescape(notice[s:e])
            match.append((link, name, date))
        match.reverse()
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
