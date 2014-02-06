# -*- coding:utf-8 -*-
import datetime
import random
import ftplib
import wx

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
    f = open("weixin/lottery", "a")
    time_str = datetime.datetime.now().strftime('%Y-%m-%d--%H:%M:%S')
    f.write((userid + " " + time_str + " " + name + "\n").encode('utf8'))
    f.close()

def getResult(count, seconds = 3600):
    f = open("weixin/lottery", "r")
    now = datetime.datetime.now()
    cand = []
    idset = set()
    for line in f:
        l = line.split()
        time = datetime.datetime.strptime(l[1], '%Y-%m-%d--%H:%M:%S')
        if (now - time).total_seconds() < seconds and l[0] not in idset:
            cand.append(l[2])
            idset.add(l[0])
    if (len(cand) < count):
        count = len(cand)
    r = random.sample(cand, count)
    f.close()
    f = open('weixin/lottery.html', 'w')
    f.writelines(r)
    f.close()

def upload():
    ftp = ftplib.FTP()
    ftp.connect('home.ustc.edu.cn', '21')
    ftp.login(wx.ftp_name, wx.ftp_password)
    ftp.cwd('public_html')
    ftp.storbinary('STOR lottery.html', open('weixin/lottery.html'))
    ftp.close()
