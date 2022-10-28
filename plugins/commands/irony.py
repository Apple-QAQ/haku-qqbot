"""
反话（复习字符串切片）
"""


def run(message):
    meg = message.message.split()[1:]
    tmp = " ".join(meg)
    ret = ""
    for i in tmp:
        if i == " ":
            pass
        else:
            ret += i  # 检测是否是空字符
    if (('[' in ret) and (']' not in ret)) or (('[' not in ret) and (']' in ret)):
        pass  # 防止cq码误判断
    elif "[CQ:at,qq=" in ret:
        ret = ret.split("[CQ:at,qq=" and ']')  # 防止cq码误判断
        del ret[0]
    ret = "".join(ret)[::-1]
    if ret == '':
        return '猫猫认为.irony需要跟随参数的说~'
    else:
        return ret
