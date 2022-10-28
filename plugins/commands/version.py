"""
获取版本号
"""
import requests

import haku.config

url: str


def config():
    global url
    cfg = haku.config.Config()
    url = f'http://{cfg.get_listen_host()}:{cfg.get_listen_port()}/version'


def run(message) -> str:
    meg = message.message.split()[1:]
    end = ''
    for i in meg:
        if i == " ":
            pass
        else:
            end += i
    if end != '':
        return '猫猫认为.version不需要跟随参数的说~'
    else:
        try:
            resp = requests.get(url=url, timeout=5)
        except Exception as e:
            haku_bot_ver = f'获取版本号失败 {e}'
        else:
            if resp.status_code == 200:
                haku_bot_ver = resp.text
            else:
                haku_bot_ver = '获取版本号失败'

        return \
f'''机器人的名字是 {haku.config.Config().get_bot_name()} 的说~
haku_bot 框架底层版本号：{haku_bot_ver}
bot 开发者: [CQ:at,qq=3034582021]
机器人的主人是[CQ:at,qq=[CQ:at,qq={haku.config.Config().get_admin_qq_list()[0]}]

bot开发者的Github: 
    https://github.com/apple-qaq/

感谢@白狐狐 提供底层框架，他的GitHub: 
    https://github.com/weilinfox/
感谢@白狐狐 和@✪sheip9 提供的服务器！！！'''
