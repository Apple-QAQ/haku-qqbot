import api.gocqhttp
import data.log


def run(message):
    if message.is_private_message() is True:
        return "你是笨蛋嘛！这是私聊哇！"
    # else:
    help_msg = ":: 取消禁言(仅管理员与群主可用)\n" \
               "   .unmute <user_id>" \
               "\n" \
               "tip:\n" \
               "    · user_id 可以直接 at"

    member_list = api.gocqhttp.get_group_member_list(message.group_id)[1]["data"]
    data.log.get_logger().info(member_list)
    owner_and_admin_list = []

    for i in member_list:
        if i["role"] == "owner" or i["role"] == "admin":
            owner_and_admin_list.append(i["user_id"])

    if message.self_id not in owner_and_admin_list:
        return f"{help_msg}\n" \
               f"⇒ 机器人无管理员权限，暂时无法解禁"

    command = message.message.split(" ")[1:]

    if len(command) == 0 or command[0].upper() == "HELP":
        return help_msg

    if message.user_id not in owner_and_admin_list:
        return "呜喵……你不是管理员或者群主哇……"

    try:
        unmute_qq_id = int(command[0])
    except ValueError:
        import re
        try:
            mute_qq_id_tmp = re.findall(r"\[CQ:at,qq=(\d*)]", command[0])
            if len(mute_qq_id_tmp) == 0:
                return help_msg
            unmute_qq_id = int(mute_qq_id_tmp[0])
        except ValueError:
            return help_msg

    if unmute_qq_id in owner_and_admin_list:
        return "喵？你是想要禁言管理员或者是群主？？？"

    user_list = []

    for i in member_list:
        user_list.append(i["user_id"])

    if unmute_qq_id not in user_list:
        return f"呜喵……没有 {unmute_qq_id} 这个人……"

    api.gocqhttp.group_ban_cancel(group_id=message.group_id, user_id=unmute_qq_id)
    return f":: 解禁成功\n" \
           f"用户: {unmute_qq_id}"
