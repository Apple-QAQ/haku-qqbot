"""
今天来到了……
"""
import api.gocqhttp
import requests

URL = "http://api.ay1.us/randomdj?g=1"


def run(message):
    if message.is_group_message():
        api.gocqhttp.send_group_msg(group_id=message.group_id, message="⇒ 丁真图 Api 有时很慢，请耐心等待，不要重复发送~")
    else:
        api.gocqhttp.send_private_msg(user_id=message.user_id, message="⇒ 丁真图 Api 有时很慢，请耐心等待，不要重复发送~")

    url = requests.get(url=URL).url.replace("raw.githubusercontent.com", "raw.kgithub.com")

    if message.is_group_message():
        api.gocqhttp.send_group_msg(group_id=message.group_id, message="→ 图片已获取，正在发送中")
    else:
        api.gocqhttp.send_private_msg(user_id=message.user_id, message="→ 图片已获取，正在发送中")
    ret = f'[CQ:image,file={url},cache=0]\n' \
          f'→ 感谢@aya 的api!'

    return ret
