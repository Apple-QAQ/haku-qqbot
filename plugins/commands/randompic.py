"""
随机萝莉图
"""
from random import randint

url = ['[CQ:image,file=https://gallery.inuyasha.love/random,cache=0]\n'
       '→ 感谢@白狐狐提供技术支持',
       "[CQ:image,file=https://iw233.cn/API/Random.php,cache=0]\n"
       "→ API来源: https://iw233.cn/"]


def run(message) -> str:
    meg = message.message.split()[1:]
    rand = randint(0, 1)
    if len(meg) == 0:
        return url[rand]
    else:
        if meg[0] == "loli":
            return url[0]
        elif meg[0] == "pic" or meg[0] == "picture":
            return url[1]
        else:
            return ":: 随机图片\n" \
                   "    .randompic → 使用随机 Api\n" \
                   "    .randompic loli → 使用以前 .loli 的 Api\n" \
                   "    .randompic pic\n" \
                   "    .randompic picture → 使用 https://iw233.cn/ 提供的 Api"
