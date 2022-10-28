url = "https://www.adorable0v0.top/api/"


def run(message):
    meg = "".join(message.message.split()[1:])
    for _ in meg:
        meg.replace(" ", "")
    if meg != '':
        return '→ 猫猫认为.loli不需要跟随参数的说~'
    return f'[CQ:image,file={url},cache=0]' \
           f'→ 感谢@拉菲艾拉La_Pluma 的api!'
