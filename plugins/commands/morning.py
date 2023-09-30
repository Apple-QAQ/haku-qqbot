"""
查询群聊问早情况
"""
import json

from api import gocqhttp

HELP_MSG = ":: 查询群聊问早情况\n" \
           " .morning → 查询"


def __nick_name(qq_id):
    return gocqhttp.get_stranger_info(qq_id)[1]["data"]["nickname"]


def run(message):
    if message.is_private_message():
        return "⇒ 啊哦，这个指令只能在群聊里使用哦……"
    elif "help" in message.message:
        return HELP_MSG

    try:
        with open("files/commands/good-morning.json", "r") as file:
            morning = json.loads(file.read())['group']

        if str(message.group_id) not in morning:
            return "→ 群内还没有问早过哦~请发送 '早' 试试看吧！"

        ret = "→ 群内问早排名:"

        for index, user in enumerate(morning[str(message.group_id)]):
            index += 1
            ret += f"\n{str(index).rjust(2, '0')} | {__nick_name(user)} ({user})"
            if index == 10:
                ret += f"\n11 | ... (仅显示前10个问早的用户)"
                break

        return ret
    except:
        return "→ 群内还没有问早过哦~请发送 '早' 试试看吧！"
