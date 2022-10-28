import api.gocqhttp
import data.log
import time
import random


def run(message):
    if message.is_private_message() is False:
        return ""
    send_message: str = message.message.replace(".shout", "", 1)

    if send_message[0] == "\n":
        send_message = send_message.replace("\n", "", 1)

    if send_message[0] == " ":
        send_message = send_message.replace(" ", "", 1)

    already_join_group_list = []

    for i in api.gocqhttp.get_group_list()[1]["data"]:
        already_join_group_list += [i["group_id"]]

    api.gocqhttp.send_private_msg(user_id=message.user_id, message=f"⇒ 请等待 60 秒，如果有改变请迅速前往服务器关闭进程并重启！\n\n"
                                                                   f"消息为:\n"
                                                                   f"{send_message}")

    time.sleep(60)
    api.gocqhttp.send_private_msg(user_id=message.user_id, message="⇒ 开始发送")
    for i in already_join_group_list:
        time.sleep(random.randint(1, 2))
        api.gocqhttp.send_group_msg(i, send_message)

    api.gocqhttp.send_private_msg(user_id=message.user_id, message="→ 全部发送完毕！！")
    data.log.get_logger().info(f"全部发送完毕\n消息:\n{send_message}")
