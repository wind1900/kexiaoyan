# -*- coding: utf-8 -*-

from utils import *
from django.template import Template, Context
import requests
import re
import datetime

template = "{{date.month}}月{{date.day}}日{{weather}}，{{temp}}"

def update():
    filename = get_filename(__name__)
    if need_update(filename):
        templates = [Template(template) for i in range(2)]
        contexts = [Context() for i in range(2)]
        args = ({}, {})
        today = datetime.date.today()
        request = requests.get("http://www.weather.com.cn/html/weather/101220101.shtml")
        content = request.content
        s = content.find('day 2')
        e = content.find('day 4')
        sc = content[s:e]
        tr_pattern = re.compile(r'<tr>.*?</tr>', re.S)
        td_pattern = re.compile(r'<td.*?</td>', re.S)
        weath_pattern = re.compile(r'blank">(.*)</a>')
        temp_pattern = re.compile(r'<strong>(.*)</strong>')
        tr = tr_pattern.findall(sc)
        for (i, day) in enumerate(tr[::2]):
            td = td_pattern.findall(day)
            args[i]['day_weather'] = weath_pattern.search(td[3]).group(1)
            args[i]['day_temp'] = temp_pattern.search(td[4]).group(1)
        for (i, night) in enumerate(tr[1::2]):
            td = td_pattern.findall(night)
            args[i]['night_weather'] = weath_pattern.search(td[2]).group(1)
            args[i]['night_temp'] = temp_pattern.search(td[3]).group(1)
        for (i, args) in enumerate(args):
            if args['day_weather'] == args['night_weather']:
                weather = args['day_weather']
            else:
                weather = args['day_weather'] + '转' + args['night_weather']
            contexts[i]['weather'] = weather
            if args['day_temp'] == args['night_temp']:
                temp = args['day_temp']
            else:
                temp = args['day_temp'][:-3] + '~' + args['night_temp']
            contexts[i]['temp'] = temp
            contexts[i]['date'] = today + datetime.timedelta(days=i+1)
        content = u'；'.join(template.render(Context(context)) for template, context in zip(templates, contexts))
        f = open(filename, 'w')
        f.write(content.encode('utf8'))
        f.close()
    else:
        f = open(filename)
        content = f.read()
        f.close()
    return content
