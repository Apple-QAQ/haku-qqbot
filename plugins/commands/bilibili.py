import re
import time

import bilibili_api
import bilibili_api.app

import data.log

verify = bilibili_api.Verify(
    sessdata="fb3beb5a%2C1673250422%2Caf711%2A71",
    buvid3="0F85A2BA-D857-CA43-75E8-1BF6F8EB479B32985infoc",
    csrf="771967e186514f37594ec529cf19de56",
)


def b23tv_to_bv(url):
    import requests
    try:
        get = requests.get(url, timeout=5).url
    except requests.exceptions.ConnectTimeout as e:
        data.log.get_logger().error(f"bilibili changeb23tv error: {e}")
        return ""
    ret = re.search(r"BV?[a-zA-Z\d]*", get).group()
    return ret


class GetLive:
    def __init__(self, room_id: int):

        self.info = bilibili_api.live.get_room_info(room_real_id=room_id, verify=verify)

    def useful_get_info(self):
        """
        获取一些常用的
        """
        get_live_info = self.info
        if get_live_info['room_info']['live_status'] == 0:
            status = "未在直播"
        else:
            status = "正在直播"

        room_picture = get_live_info['room_info']['cover']
        room_description = get_live_info['room_info']['description']
        room_title = get_live_info['room_info']['title']
        room_id = get_live_info['room_info']['room_id']
        area = get_live_info['room_info']['area_name']
        user_name = get_live_info['anchor_info']['base_info']['uname']
        room_link = f"https://live.bilibili.com/{room_id}"
        return {"status": status, "picture": room_picture, "link": room_link, "description": room_description,
                "title": room_title, "area": area, "user_name": user_name}


class GetVideo:
    def __init__(self, which_video: str, video_id: int or str):
        if which_video.upper() == "AV" and type(video_id) == int:
            self.info = bilibili_api.video.get_video_info(aid=video_id, verify=verify)
        else:
            self.info = bilibili_api.video.get_video_info(bvid=video_id, verify=verify)

    def useful_get_info(self):
        bv_id = self.info['bvid']
        av_id = f"AV{self.info['aid']}"
        title = self.info['title']
        picture = self.info['pic']
        video_time = time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime(self.info['pubdate'] + 28800))
        up = self.info["owner"]['name']
        viewer = self.info["stat"]["view"]
        danmaku = self.info["stat"]["danmaku"]
        coins = self.info["stat"]['coin']
        raw_text = "\n    ".join(self.info["desc"].split('\n'))
        return f'标题: {title}\n' \
               f'UP主: {up}\n' \
               f'时间: {video_time}\n' \
               f'{av_id}  {bv_id}\n' \
               f'------------------------' \
               f'[CQ:image,file={picture},cache=0]' \
               f'------------------------\n' \
               f'\n' \
               f'简介:\n' \
               f'    {raw_text if len(raw_text) <= 100 else f"{raw_text[0:99]} ……"}\n' \
               f'\n' \
               f'播放: {viewer if viewer < 10000 else f"{round((viewer / 10000), 1)}万"}  ' \
               f'弹幕: {danmaku if danmaku < 10000 else f"{round((danmaku / 10000), 1)}万"}  ' \
               f'投币: {coins if coins < 10000 else f"{round((coins / 10000), 1)}万"}\n\n' \
               f'https://www.bilibili.com/video/{bv_id}'


def run(message):
    ret: list = message.message.split()
    del ret[0]
    if ret[0] == "live":
        try:
            home_id = int(ret[1])
        except ValueError:
            return "⇒ id数据类型错误"
        get_info = GetLive(home_id).useful_get_info()

        if len(ret) >= 3:
            if "".join(ret[2:]) == "auto":  # 自动
                group = message.group_id
                is_send = {group: False}
                i_wanna_send = is_send[group]

                try:
                    with open(f"files/commands/bilibiliLiveAuto-{group}.txt", "r") as file:
                        info = file.read()  # 首先读取一遍文件
                        data.log.get_logger().info(f"读取成功！info: {info}")
                except FileNotFoundError:
                    with open(f"files/commands/bilibiliLiveAuto-{group}.txt", "x"):
                        data.log.get_logger().info(f"创建新文件成功～")
                    with open(f"files/commands/bilibiliLiveAuto-{group}.txt", "r") as file:
                        info = file.read()  # 首先读取一遍文件
                        data.log.get_logger().info(f"读取成功！info: {info}")

                if f"{get_info['user_name']}-{get_info['status']}" != info and i_wanna_send is False:
                    with open(f"files/commands/bilibiliLiveAuto-{group}.txt", "w") as file:
                        file.write(f"{get_info['user_name']}-{get_info['status']}")  # 覆写
                    is_send.update({group: True})
                    data.log.get_logger().info(f"更新成功，组字典: {is_send}")

                elif f"{get_info['user_name']}-{get_info['status']}" == info and i_wanna_send is True:
                    with open(f"files/commands/bilibiliLiveAuto-{group}.txt", "w") as file:
                        file.write(f"{get_info['user_name']}-{get_info['status']}")  # 覆写
                    is_send.update({group: False})
                    data.log.get_logger().info(f"更新成功，组字典: {is_send}")

                elif f"{get_info['user_name']}-{get_info['status']}" == info and i_wanna_send is False:
                    data.log.get_logger().info(f"群 {group} 已推送过")
                    return ""

                else:  # 不会用到
                    data.log.get_logger().info("发生严重错误！请检查代码！")

                i_wanna_send = is_send[group]

                if i_wanna_send:
                    if get_info['description'].replace(" ", "").replace("\n", "") == "":
                        description = "无"
                    else:
                        description = get_info['description']

                    return f"直播状态提醒！\n" \
                           f"--------------------------------------\n" \
                           f"[CQ:image,file={get_info['picture']},cache=0]" \
                           f"--------------------------------------\n" \
                           f"主播: {get_info['user_name']}\n" \
                           f"标题: {get_info['title']}\n" \
                           f"状态: {get_info['status']}\n" \
                           f"分区: {get_info['area']}\n" \
                           f"简介: \n" \
                           f"    {description}\n" \
                           f"{get_info['link']}"

            else:
                return "你在瞎写什么！"

        else:
            if get_info['description'].replace(" ", "").replace("\n", "") == "":
                description = "无"
            else:
                description = get_info['description']

            return f"[CQ:image,file={get_info['picture']},cache=0]" \
                   f"--------------------------------------\n" \
                   f"主播: {get_info['user_name']}\n" \
                   f"标题: {get_info['title']}\n" \
                   f"状态: {get_info['status']}\n" \
                   f"分区: {get_info['area']}\n" \
                   f"简介: \n" \
                   f"    {description}\n" \
                   f"{get_info['link']}"
    #############################
    elif ret[0] == "video":
        if "AV" in "".join(ret[1:]):
            return GetVideo("AV", int("".join(ret[1:]).replace("AV", ""))).useful_get_info()
        elif "BV" in "".join(ret[1:]):
            return GetVideo("BV", "".join(ret[1:])).useful_get_info()
        else:
            return "⇒ 请检查您输入的内容"
    #############################
    else:
        return "⇒ 有待完善"
