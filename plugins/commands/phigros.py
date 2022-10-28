import requests
import data.log
import re

url_update = "https://www.taptap.com/webapiv2/apk/v1/list-by-app?app_id=165287&X-UA=V%3D1%26PN%3DWebApp%26LANG" \
             "%3Dzh_CN%26VN_CODE%3D76%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dfac371ef-3822-44f6" \
             "-8eb2-ccaa88629e00%26DT%3DPC%26OS%3DLinux%26OSV%3D5.18.2"

headers = {
    'cookie': 'apk_download_url_postfix=/seo-google; _gid=GA1.2.215085494.1654847884; _ga=GA1.1.983718502.1654847884; '
              '_ga_6G9NWP07QM=GS1.1.1654847885.1.1.1654850442.0; '
              'acw_tc=2760829516548587781995104e158bf1030400cbd36dd67a0c088592e03fc6; '
              'XSRF-TOKEN=eyJpdiI6IjQ4bnlwVjUzQXhkTmt4ZWJmQTFhUUE9PSIsInZhbHVlIjoiTUxzVHRlZFlRTWs5ZXR5dVdGRFlmeENuV0Iw'
              'Q09Ga1dFZG5CeDFcL1Z1MTU3SGRmMDJ6S20wS2FNdWZoQTBURUwyUjZmRVBnaFwvUHhMR3Z5elpDaXlnUT09IiwibWFjIjoiOTJkY2M0'
              'ODAzNDBhYjJhY2IzMmYyYzIxZmYzMTQ3Y2M4MzM0ZDY1YTYyNWY4YzJkYThjOWFjYzRjY2QwZmE4NyJ9; tap_sess=eyJpdiI6ImZ4O'
              'Dc5bGtGRFRZSE10N01ibVhiV1E9PSIsInZhbHVlIjoiMVJqY1pOcWxyVld6bktSSk5vMlNMVFdmRUs0K3pvd25VNjhROUphenFZalRJU'
              'TM0WmNDd25sbm9ac2c5N0RjU2NLMTNVcUcrMHJac1wvMDhsMlNRVzdBPT0iLCJtYWMiOiJmZjE5MmMyYTkxNDk3NzBiMDUwODQ0OTg5M'
              'jQ0ZTJkNjk3MmEwODAwOGRhMDE4MTMxNTRkNTViODVhNjk3YWZjIn0%3D',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 '
                  'Safari/537.36 Edg/102.0.1245.33'
}


def run(message):
    user_input = message.message.split(" ")[1:]
    try:
        get_update_info_json = requests.get(url=url_update, timeout=5, headers=headers)
    except requests.exceptions.ConnectTimeout as e:
        data.log.get_logger().error(f"Phigros requests error: {e}")
        return ""
    if get_update_info_json:
        get_update_information = get_update_info_json.json()['data']['list'][0]
        if message.is_group_message():
            group = message.group_id
            is_send = {group: False}
            i_wanna_send = is_send[group]
            try:
                with open(f"files/commands/phigros-send-{group}.txt", "r") as file:
                    info = file.read()
                    data.log.get_logger().info(f"读取成功！info: {info}")
            except FileNotFoundError:
                with open(f"files/commands/phigros-send-{group}.txt", "x"):
                    data.log.get_logger().info(f"创建新文件成功～")
                with open(f"files/commands/phigros-send-{group}.txt", "r") as file:
                    info = file.read()
                    data.log.get_logger().info(f"读取成功！info: {info}")

            if f"{get_update_information['version_label']}" != info and i_wanna_send is False:
                with open(f"files/commands/phigros-send-{group}.txt", "w") as file:
                    file.write(f"{get_update_information['version_label']}")  # 覆写
                is_send.update({group: True})
                data.log.get_logger().info(f"更新成功，组字典: {is_send}")

            elif f"{get_update_information['version_label']}" == info and i_wanna_send is True:
                with open(f"files/commands/phigros-send-{group}.txt", "w") as file:
                    file.write(f"{get_update_information['version_label']}")  # 覆写
                is_send.update({group: False})
                data.log.get_logger().info(f"更新成功，组字典: {is_send}")

            elif f"{get_update_information['version_label']}" == info and i_wanna_send is False:
                data.log.get_logger().info(f"群 {group} 已推送过")

            else:  # 不会用到
                data.log.get_logger().info("发生严重错误！请检查代码！")

            if len(user_input) == 0:
                i_wanna_send = True
            elif "auto" in user_input:
                i_wanna_send = is_send[group]

        else:
            i_wanna_send = False

        if i_wanna_send:
            information = get_update_information['whatsnew']['text']
            information = information.replace("<div>", "").replace('</div>', "")
            information = re.sub(r"&\w+;", "  ", information)
            information = re.sub(r"<br*.>", "\n", information)
            ret = []

            for i in information.split("\n"):
                if i == "":
                    pass
                else:
                    ret += [f"   {i}"]

            ret = "\n".join(ret)

            return f":: 检测到 Phigros 更新!\n" \
                   f"→ 更新版本: {get_update_information['version_label']}\n" \
                   f"→ 更新内容: \n" \
                   f"{ret}"
