"""
改群聊指定人名字
"""
from api import gocqhttp


def run(message):
    command = message.message.split()
    del command[0]
    if len(command) == 0:
        return ":: 修改群员名片\n" \
               "    .changename <userid> <card>"
    if command[2].upper() == "YCXMODE":
        import time
        import random
        while True:
            gocqhttp.set_group_card(group_id=message.group_id, user_id=int(command[0]), card=command[1])
            time.sleep(random.randint(1, 5))
    try:
        gocqhttp.set_group_card(group_id=message.group_id, user_id=int(command[0]), card=command[1])
    except ValueError:
        return "发生错误！请检查您的<userid>部分"
