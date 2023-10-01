import time

import data.log
import html
import re
import api.gocqhttp
import json

import haku.config


def extract_json(s: str):
    __i = s.index('{')
    __count = 1  # 当前所在嵌套深度，即还没闭合的'{'个数
    __j = 0
    for __j, __c in enumerate(s[__i + 1:], start=__i + 1):
        if __c == '}':
            __count -= 1
        elif __c == '{':
            __count += 1
        if __count == 0:
            break
    assert (__count == 0)  # 检查是否找到最后一个'}'
    return s[__i:__j + 1]


###############
def plugins(self, block_default_config):
    """
    处理不是 . 开头的命令
    """
    # 检测是否因为调用插件而复读
    repeat = False

    bilibili_catch_black_group = block_default_config["bilibili_catch_black_group"]
    data.log.get_logger().info(f"bilibili_catch_black_group: {bilibili_catch_black_group}")

    new_cache = {'msg': self.message, 'id': self.user_id, 'time': self.time}
    if self.group_id in self.group_msg_cache_1.keys():
        cached = self.group_msg_cache_1[self.group_id]
        if self.message == cached['msg'] and self.self_id == cached['id']:
            # 已经复读过了
            pass
        else:
            self.group_msg_cache_2[self.group_id] = cached
            if self.user_id != cached['id'] \
                    and self.message == cached['msg'] and self.time - cached['time'] < 60:
                # 相同 id 和超过时效 60s 的都不复读
                # 将缓存消息的 qq id 改为 bot 自身 表示已经复读过了
                new_cache['id'] = self.self_id
                repeat = True
            self.group_msg_cache_1[self.group_id] = new_cache
    else:
        self.group_msg_cache_1[self.group_id] = new_cache

    if self.group_id not in bilibili_catch_black_group:
        message = self.message.replace("\\/", "/")
        if "https://b23.tv/" in html.unescape(message):
            bv_id = ""
            try:
                from plugins.commands import bilibili
                where_is_b23 = re.search(r'(https://b23.tv/?[a-zA-Z\d]*)', message).group()
                bv_id = bilibili.b23tv_to_bv(where_is_b23)
                ret = bilibili.GetVideo("BV", bv_id).useful_get_info()
                api.gocqhttp.send_group_msg(self.group_id, ret)
            except Exception as e:
                data.log.get_logger().error(f"\n{bv_id}\n{e}")
        ###################################################
    if "{" in self.message and "}" in self.message and ":" in self.message:
        __blacklist = [
            '"QQ小"',
            '"app"'
        ]
        for __i in __blacklist:
            if __i in self.message:
                break
        else:
            try:
                __message = extract_json(html.unescape(self.message))

                data.log.get_logger().info(__message)
                __ret = str(json.dumps(json.loads(__message), indent=2, ensure_ascii=False))

                api.gocqhttp.send_group_msg(self.group_id, f"检测到json，格式化输出如下:\n\n{__ret}")
            except Exception as e:
                data.log.get_logger().error(e)
    elif f"[CQ:at,qq={api.gocqhttp.get_login_info()[1]['data']['user_id']}]" in self.message and \
            "[CQ:reply,id=" not in self.message:
        api.gocqhttp.send_group_msg(self.group_id,
                                    f"[CQ:at,qq={haku.config.Config().get_admin_qq_list()[0]}]\n"
                                    f"嘛……如果想要看用法的的话就直接.help捏~")

    # Morning
    elif "早" == self.message:
        now_time = time.localtime()
        try:
            with open(f"files/commands/good-morning.json", "r") as file:
                read = json.loads(file.read())
                data.log.get_logger().info(f"读取成功！info: {read}")
        except Exception as e:
            with open(f"files/commands/good-morning.json", "w") as file:
                file.write(json.dumps({"date": now_time[0:3]}, indent=2, ensure_ascii=False))
                data.log.get_logger().info(f"创建新文件成功！错误: \n{e}")
            with open(f"files/commands/good-morning.json", "r") as file:
                read = json.loads(file.read())
                data.log.get_logger().info(f"读取成功！info: {read}")

        if read['date'] == list(now_time[0:3]):  # 第二天重置时间
            data.log.get_logger().info("不是第二天")
        else:
            with open(f"files/commands/good-morning.json", "w") as file:
                file.write(json.dumps({"date": now_time[0:3]}, indent=2, ensure_ascii=False))
                data.log.get_logger().info("在第二天覆写文件成功！")
            with open(f"files/commands/good-morning.json", "r") as file:
                read = json.loads(file.read())
                data.log.get_logger().info(read)

        if not read.get("group"):
            with open(f"files/commands/good-morning.json", "r") as file:
                read = json.loads(file.read())
            with open(f"files/commands/good-morning.json", "w") as file:
                read.update({"group": {}})
                file.write(json.dumps(read, indent=2, ensure_ascii=False))
                data.log.get_logger().info(f"初始化group组成功！")
            with open(f"files/commands/good-morning.json", "r") as file:
                read = json.loads(file.read())
                data.log.get_logger().info(read)

        group_id = str(self.group_id)

        if group_id not in read.get("group"):
            with open(f"files/commands/good-morning.json", "r") as file:
                read = json.loads(file.read())
            with open(f"files/commands/good-morning.json", "w") as file:
                if self.group_id not in read.get("group"):
                    read['group'].update({self.group_id: []})
                    file.write(json.dumps(read, indent=2, ensure_ascii=False))
                    data.log.get_logger().info(f"群组 {self.group_id} 初始化成功")

        with open(f"files/commands/good-morning.json", "r") as file:
            read = json.loads(file.read())
        with open(f"files/commands/good-morning.json", "w") as file:
            if self.user_id not in read['group'][group_id]:
                if len(read['group'][group_id]) == 0:
                    ret = f"早哇~你是今天群里最早问早的喵~"
                else:
                    ret = f"早~你是今天第 {len(read['group'][group_id]) + 1} 个问早的~"
                api.gocqhttp.send_group_msg(self.group_id, ret)
                read['group'][group_id].append(self.user_id)
            else:
                api.gocqhttp.send_group_msg(self.group_id, f"[CQ:at,qq={self.user_id}]，你今天问过早啦~")
            file.write(json.dumps(read, indent=2, ensure_ascii=False))
            
    if repeat:
        if self.user_id == self.group_msg_cache_1[self.group_id]['id']:
            pass
        else:
            api.gocqhttp.send_group_msg(self.group_id, self.message)
