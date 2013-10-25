#-*-coding:utf-8-*-

import requests
import random

class SimSimi:

    def __init__(self):
        self.chat_url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'

    def getSimSimiResult(self, message):
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'})
        session.headers.update({'X-Requested-With': 'XMLHttpRequest'})
        session.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})
        session.headers.update({'Accept-Encoding': 'gzip,deflate,sdch'})
        session.headers.update({'Accept-Language': 'zh-CN'})
        session.headers.update({'Connection': 'keep-alive'})
        session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        session.get('http://www.simsimi.com/talk.htm')
        session.headers.update({'Referer': 'http://www.simsimi.com/talk.htm'})
        session.get('http://www.simsimi.com/talk.htm?lc=ch', cookies = {'sagree':'true'})
        session.headers.update({'Referer': 'http://www.simsimi.com/talk.htm?lc=ch'})
        r = session.get(self.chat_url % message)
        return r.json()

    def chat(self, message=''):
        if message:
            r = self.getSimSimiResult(message)
            try:
                answer = r['response'] # unicode(r['response'], 'utf-8')
                return answer # .encode('utf-8')
            except:
                return random.choice(['呵呵', '。。。', '= =', '=。='])
        else:
            return '叫我干嘛'

simsimi = SimSimi()

def handle(data):
    return simsimi.chat(data)

if __name__ == '__main__':
    print handle('hello')
    print handle(u'最后一个问题')
    print handle(u'你好啊')
