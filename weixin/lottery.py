# -*- coding:utf-8 -*-
import datetime
import random
import ftplib
import wx
import os

def handle(msg):
    if msg['Content'][:2] == u'加入':
        addUser(msg['Content'][2:], msg['FromUserName'])
        return u'欢迎加入研会'
    elif msg['Content'][:2] == u'抽奖':
        getResult(int(msg['Content'][2:]))
        upload()
        return 'OK'
    return None

def addUser(name, userid):
    f = open("weixin/lottery/" + userid, "w")
    f.write(name.encode('utf8'))
    f.write('\n')
    f.close()

def getResult(count, seconds = 900):
    now = datetime.datetime.now()
    cand = []
    for filename in os.listdir("weixin/lottery"):
        filename = "weixin/lottery/" + filename
        try:
            modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        except:
            continue
        if (now - modify_time).total_seconds() < seconds:
            f = open(filename)
            cand.append(f.readline().rstrip())
            f.close()

    if (len(cand) < count):
        count = len(cand)
    r = random.sample(cand, count)
    f = open('weixin/lottery.html', 'w')
    f.write('<html>')
    f.write('<head><meta http-equiv="content-type" content="text/html; charset=UTF-8"/></head>\n')
    f.write('<body>\n')
    f.writelines(r)
    f.write('</body></html>')
    f.close()

def upload():
    ftp = ftplib.FTP()
    ftp.connect('home.ustc.edu.cn', '21')
    ftp.login(wx.ftp_name, wx.ftp_password)
    ftp.cwd('public_html')
    ftp.storbinary('STOR lottery.html', open('weixin/lottery.html'))
    ftp.close()
