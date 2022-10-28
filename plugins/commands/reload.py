"""
本地重载插件
"""
from handlers.message import Message, Plugin


def run(message: Message) -> str:
    meg = message.message.split()[1:]
    end = ''
    for i in meg:
        if i == " ":
            pass
        else:
            end += i
    if end != '':
        return ':: 猫猫认为.reload不需要跟随参数的说~'
    else:
        try:
            plugin = Plugin()
            plugin.reload()
        except:
            return ':: Error to reload.'
        return ':: Reload successfully.'
