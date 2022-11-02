"""
Arcaea 查询
TODO: 完成所有功能
"""
from typing import Tuple

import haku.config
from api import arcaea as arc
from data import log

token = haku.config.Config().get_key("AUA_token")
arcaea = arc.Arcaea(aua_token=token)
help_meg = "提示 👉 使用本功能机器人会记录您的账号信息\n" \
           ":: arcaea 查询\n" \
           "    .arcaea bind <ArcaeaID> → 绑定账号(目前仅支持ID)\n" \
           "    .arcaea unbind → 解绑账号\n" \
           "    ^.arcaea account → 查看账号信息\n" \
           "    *.arcaea b30 → 查询b30\n" \
           "    *.arcaea r10 → 查询r10\n" \
           "    ^.arcaea ptt → 查询ptt\n" \
           "    ^.arcaea song <song> → 查询歌曲信息\n" \
           "\n" \
           "感谢 @Aw.0000 提供的 AUA\n" \
           "-备注: '^'为开发进度一半，'*'为未开发"
file_dir = "files/commands/arcaea_account.yaml"


def format_arcaea_id(arcaea_id):
    return str(arcaea_id).rjust(9, '0')


def __read() -> list:
    with open(file_dir, "r") as __file:
        info = __file.read().split("\n")[:-1]
    ret = []

    for i in info:
        temp_lst = []

        for n in i.split(": "):
            temp_lst.append(int(n))

        ret.append(temp_lst)

    return ret


def __already_bind(qq_id, all_account_file) -> Tuple[bool, int]:
    for i in all_account_file:
        if qq_id in i:
            return True, i[-1]
    return False, -1


def __make():
    with open(file_dir, "x"):
        pass
    log.get_logger().info("新建文件成功")
    return "⇒ 新建文件成功"


def __add(qq_id: int, arcaea_id: int):
    with open(file_dir, "a") as __file:
        __ = __file.write(f"{qq_id}: {arcaea_id}\n")
    return True, "账号已成功绑定"


def __del(qq_id: int):
    info = __read()
    already_del = False

    for index, i in enumerate(info):
        if qq_id in i:
            already_del = True
            del_account = i[-1]
            del info[index]
            with open(file_dir, "w"):
                pass
            break

    if already_del:
        for w in info:
            __add(w[0], w[-1])
        return already_del, del_account

    return already_del, None


def run(message):
    # 初始化
    try:
        account = __read()
    except FileNotFoundError:
        __make()
        log.get_logger().info("新建文件完毕")
        account = __read()
    already_bind = __already_bind(qq_id=message.user_id, all_account_file=account)
    command = message.message.split(" ")[1:]

    if len(command) == 0:
        return help_meg
    else:
        first_command = command[0].upper()

    if first_command == "BIND":
        if len(command) == 1:
            return help_meg
        try:
            arcaea_id = ''.join(command[1:])
            if len(arcaea_id) != 9:
                return "→ ArcaeaID 的长度应该为 9 位数"
            arcaea_id = int(arcaea_id)
        except ValueError:
            return "⇒ 错误: 目前不支持账号名称"
        if already_bind[0]:
            return f"→ 您已经绑定过了\n" \
                   f"账号id: {format_arcaea_id(already_bind[-1])}\n" \
                   f"账号名称: {arcaea.get_user_info(already_bind[-1])[-1]['content']['account_info']['name']}"

        ret = __add(qq_id=message.user_id, arcaea_id=arcaea_id)

        return f"→ 绑定成功！\n" \
               f"账号昵称: {arcaea.get_user_info(arcaea_id)[-1]['content']['account_info']['name']}" \
            if ret[0] else "⇒ 未知错误"

    elif first_command == "UNBIND":
        if not already_bind[0]:
            return "⇒ 您还未绑定账号，请绑定好再试罢~"
        ret = __del(message.user_id)
        return f"→ 已解绑!\n" \
               f"账号id: {format_arcaea_id(ret[-1])}\n" \
               f"账号昵称: {arcaea.get_user_info(ret[-1])[-1]['content']['account_info']['name']}" \
            if ret[0] else "⇒ 未知错误"

    elif first_command == "SONG":
        search = " ".join(command[1:])
        info = arcaea.get_song_info(search)  # 查询歌曲
        all_difficulty = ['PST', 'PRS', 'FTR', 'BYD']  # 难度
        if not info[0]:
            return "⇒ 未知错误"
        info = info[-1]
        if info["status"] == -8:
            ret = f":: 关于 {search} 有很多种结果，您想要的是哪个?\n"
            for n in info['content']['songs']:
                ret += f"→ {n}\n"
            ret += "    请选择相应的乐曲再试试罢~"
            return ret
        elif info['status'] == 0:
            music_info = info['content']
            difficulties = ''
            for index, i in enumerate(music_info['difficulties']):
                difficulties += f"\n    {all_difficulty[index]}: {i['difficulty'] / 2}"
            return f"歌名: {music_info['difficulties'][0]['name_en']}\n" \
                   f"曲师: {music_info['difficulties'][0]['artist']}\n" \
                   f"BPM: {music_info['difficulties'][0]['bpm']}\n" \
                   f"难度: {difficulties}"
        else:
            return "⇒ 抱歉，猫猫没有找到这首歌，能否换个表达方式？"

    elif first_command == "ACCOUNT":
        if already_bind[0]:
            info = arcaea.get_user_info(already_bind[-1])[-1]['content']['account_info']
            return f"→ 查询账号\n" \
                   f"账号id: {format_arcaea_id(already_bind[-1])}\n" \
                   f"账号名称: {info['name']}\n" \
                   f"您的ptt: {arcaea.get_user_info(already_bind[-1])[-1]['content']['account_info']['rating'] / 100}"
        else:
            return "⇒ 您还未绑定，请使用 .arcaea bind <ArcaeaID> 绑定账号，输入 .arcaea 获取使用帮助"

    elif first_command == "B30":
        return "*开发中……"
    elif first_command == "R10":
        return "*开发中……"
    elif first_command == "PTT":
        if already_bind[0]:
            info = arcaea.get_user_info(already_bind[-1])[-1]['content']['account_info']
            return f"→ 查询ptt:\n" \
                   f"账号id: {format_arcaea_id(already_bind[-1])}\n" \
                   f"账号名称: {info['name']}\n\n" \
                   f"您的 ptt 为: {info['rating'] / 100}"
        else:
            return "⇒ 您还未绑定，请使用 .arcaea bind <ArcaeaID> 绑定账号，输入 .arcaea 获取使用帮助"
    else:
        return help_meg
