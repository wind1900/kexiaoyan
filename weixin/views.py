# -*- coding:utf-8 -*-

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import hashlib
import time
import simimi
import xml.etree.ElementTree as ET
import wx

def verify(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')
    if signature == None:
        return False
    token = wx.token
    str_list = [token, timestamp, nonce]
    str_list.sort()
    verify_str = "".join(str_list)
    hash_str = hashlib.sha1(verify_str).hexdigest()
    if hash_str != signature:
        return False
    return True

@csrf_exempt
def main(request):
    if not verify(request):
        raise Http404
##    return HttpResponse(request.GET.get('echostr'))
    msg_root = ET.fromstring(request.body)
    msg = {}
    for child in msg_root:
        msg[child.tag] = child.text
    reply_msg = {}
    reply_msg['touser'] = msg['FromUserName']
    reply_msg['fromuser'] = msg['ToUserName']
    reply_msg['createtime'] = str(int(time.time()))
    reply_msg['content'] = simimi.handle(msg['Content'])
    if msg['MsgType'] == 'text':
        return HttpResponse(reply_text.format(**reply_msg))

    return HttpResponse("hello world")

reply_text = u'''<xml>
<ToUserName><![CDATA[{touser}]]></ToUserName>
<FromUserName><![CDATA[{fromuser}]]></FromUserName>
<CreateTime>{createtime}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
'''
