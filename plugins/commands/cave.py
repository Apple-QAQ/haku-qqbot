"""
回声洞(cave)
"""
import json
from random import randint

from api import gocqhttp

file_dir = "files/commands/cave.json"


def __new_cave(number, group_id, user_id, text) -> dict:
    ret = {
        "number": number,
        "group_id": group_id,
        "user_id": user_id,
        "text": text
    }
    return ret


def __rewrite_json(text: dict or list) -> None:
    with open(file_dir, "w") as file:
        file.write(json.dumps(text, indent=2, ensure_ascii=False))


def __secrecy(text: str):
    return f"{text[0:2]}{'*' * (len(text) - 2)}{text[-2:]}"


def __read_and_get_json() -> list:
    try:
        with open(file_dir, "r") as file:
            read = json.loads(file.read())
    except FileNotFoundError:
        __rewrite_json([])
        read = []
    return read


def __group_name(group_id):
    return gocqhttp.get_group_info(group_id=group_id)[1]['data']['group_name']


def __nick_name(user_id):
    return gocqhttp.get_stranger_info(user_id)[1]["data"]["nickname"]


def run(message):
    if message.is_private_message():
        return "⇒ 请在群组内使用此命令"
    commands = message.message.split(" ")[1:]
    get_json = __read_and_get_json()

    if len(commands) == 0:
        if len(get_json) == 0:
            return "⇒ 回声洞里还没有任何东西，快去添加罢！"
        random_cave = get_json[randint(0, len(get_json) - 1)]
        """ 
        random_cave = {
            "number": number,
            "group_id": group_id,
            "user_id": user_id,
            "text": text
        }
        """
        ret = f"回声洞 (NO.{random_cave['number']}) ——\n" \
              f"\n" \
              f"{random_cave['text']}\n" \
              f"\n" \
              f"      —— 来自群组 {__group_name(random_cave['group_id'])}" \
              f"({__secrecy(str(random_cave['group_id']))}) 的 {__nick_name(random_cave['user_id'])}" \
              f"({__secrecy(str(random_cave['user_id']))})"
    elif commands[0] == "many" or commands[0] == "much":
        ret = f"→ 当前回声洞内有 {len(get_json)} 个。"
    elif ".cave add" in message.message:
        cave_add_info = message.message.replace(".cave add ", "", 1).replace(".cave add", "", 1)
        if cave_add_info.replace(" ", "").replace("\n", "") == '':
            return "⇒ 无法添加无意义的空白消息！"
        new_cave = __new_cave(
            group_id=message.group_id,
            user_id=message.user_id,
            text=cave_add_info,
            number=len(get_json) + 1,
        )
        __rewrite_json(get_json + [new_cave])
        ret = f"→ 嗷呜~添加成功！这是第 {len(get_json) + 1} 条回声洞，消息为:\n" \
              f"{cave_add_info}"
    else:
        ret = ":: cave回声洞使用方法\n" \
              "    .cave → 查看回声洞\n" \
              "    .cave add <message> → 添加回声洞消息\n" \
              "    .cave much\n" \
              "    .cave many\n" \
              "    .cave quantity → 查看回声洞消息数量"

    return ret
