"""
什么！你居然不会百度！
"""
import base64


def run(message):
    search = message.message.split(' ', 1)
    search = search[1] if len(search) != 1 else ""
    if not search.replace(' ', ''):
        return ":: 教你百度\n" \
               "   .baidu <search> → 教你百度搜索"
    search = base64.b64encode(search.encode("utf-8")).decode('utf-8')
    return f"https://mengkunsoft.github.io/lmbtfy/?q={search}"
