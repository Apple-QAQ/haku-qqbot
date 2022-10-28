"""
一言
"""
import requests
import json

import data.log
from handlers.message import Message

myLogger = data.log.get_logger()


def run(message: Message) -> str:
    help_msg = '传入参数，猫猫会搜索以下五个类别的说~\na 动画, b 漫画\nc 文学, d 哲学\ne 诗词, f 随机(没写)'
    req = list(message.raw_message.split(' ', 1))
    if len(req) > 1:
        req[1] = req[1].strip()
    if len(req) > 1 and len(req[1]) > 0:
        url = 'https://v1.hitokoto.cn/'
        if req[1] == 'a':
            params = {'c': 'a'}
        elif req[1] == 'b':
            params = {'c': 'b'}
        elif req[1] == 'c':
            params = {'c': 'd'}
        elif req[1] == 'd':
            params = {'c': 'k'}
        elif req[1] == 'e':
            params = {'c': 'i'}
        elif req[1] == 'f':
            return "不是跟你说了没写么笨蛋！"
        else:
            ans = '狐狐是我的！谁都不许碰！\nApple_QAQ'
            return ans

        try:
            resp = requests.get(url=url, params=params, timeout=5)
            if resp.status_code == 200:
                rejson = json.loads(resp.text)
                # print(rejson)
                ans = rejson['hitokoto'] + '\n' + rejson['from']
            else:
                ans = '好像返回了奇怪的东西: ' + str(resp.status_code)
        except Exception as e:
            myLogger.exception(f'RuntimeError {e}')
            ans = '啊嘞嘞好像出错了，一定是一言炸了不关猫猫！'
    else:
        ans = help_msg

    return ans
