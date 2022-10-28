"""
网易云音乐
"""
import requests

import data.log
import api.gocqhttp
from handlers.message import Message

URL = 'https://api.inuyasha.love/netease-cloud-music/search'
myLogger = data.log.get_logger()
past = {}


def run(message: Message) -> str:
    global past
    req = message.message.split(' ')[1:]
    ans = ":: 查询歌曲\n" \
          "    .music {id} {search} → 查询音乐(网易云)"
    if len(req) == 0:
        pass
    elif "".join(req).replace(" ", "") == "":
        return "您输入了啥？"
    else:
        try:
            req[0] = int(req[0])
            if len(req) == 1 and message.message_type == "group":
                if not past.get(message.group_id):
                    return f"啊咧，群里之前没有人搜索过呢~\n" + ans
                msc_id = past[message.group_id][-1]['result']['songs'][req[0]]['id']
                api.gocqhttp.send_group_msg(message.group_id, "嘛~你的后面没跟东西嘛，那就用上次的查询吧~")
                api.gocqhttp.send_group_share_music(message.group_id, '163', msc_id)
                return ""
            elif len(req) == 1 and message.message_type == "private":
                return ans
            try:
                resp = requests.get(url=URL, params={'keywords': " ".join(req[1:])}, timeout=5)
            except Exception as e:
                myLogger.exception(f'RuntimeError {e}')
                ans = '⇒ 啊嘞嘞好像出错了'
            else:
                if resp.status_code == 200:
                    rejson = resp.json()
                    msc_id = rejson['result']['songs'][req[0]]['id']
                    if message.message_type == 'group':
                        api.gocqhttp.send_group_share_music(message.group_id, '163', msc_id)
                    elif message.message_type == 'private':
                        api.gocqhttp.send_private_share_music(message.user_id, '163', msc_id)
                    return ""
                else:
                    ans = '⇒ 好像返回了奇怪的东西: ' + str(resp.status_code)
        except ValueError:
            try:
                resp = requests.get(url=URL, params={'keywords': " ".join(req)}, timeout=5)
            except Exception as e:
                myLogger.exception(f'RuntimeError {e}')
                ans = '⇒ 啊嘞嘞好像出错了'
            else:
                if resp.status_code == 200:
                    rejson = resp.json()
                    if message.message_type == "group":
                        past.update(
                            {message.group_id: [] if not past.get(message.group_id) else past[message.group_id]}
                        )
                        past[message.group_id].append(rejson)
                    try:
                        rejson['result']
                    except KeyError:
                        return "⇒ 网易云里没有诶~"
                    if rejson['result'].get('songs'):
                        msc = rejson['result']['songs']

                        ret_list_info = "序号 | 名称 - 作者\n" \
                                        "---------------------------"

                        for index, i in enumerate(msc):
                            artists = []

                            for n in i['artists']:
                                artists.append(n["name"])

                            ret_list_info += f"\n{index} |  {i['name']} - {'/'.join(artists)}\n" \
                                             f"---------------------------"

                            if index == 9:
                                break

                        ret_list_info += "\n\n请输入: “.music 序号 您前面所输入的搜索内容”(推荐) 或者 “.music 序号”(不推荐)进行具体推送" \
                                if message.message_type == "group" else "\n\n请输入: “.music 序号 您前面所输入的搜索内容” 进行具体推送"
                        ans = ret_list_info
                    else:
                        ans = '⇒ 网易云里没有诶~'
                else:
                    ans = '⇒ 好像返回了奇怪的东西: ' + str(resp.status_code)
    return ans
