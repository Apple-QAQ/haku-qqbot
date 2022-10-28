"""
Archlinux 包查询
"""
import requests
import re
from handlers.message import Message


def search_arch(keywords: str) -> str:
    baseurl = 'https://archlinux.org'
    searchurl = '/packages/'
    params = {
        'sort': '',
        'maintainer': '',
        'flagged': '',
        'q': keywords,
    }

    try:
        res = requests.get(url=baseurl+searchurl, params=params, timeout=20)
    except requests.exceptions.ReadTimeout:
        return '→ 呜呜呜，查询超时了，一定不是猫猫的错！请再试试看~'

    if res.status_code == 200:
        restexts = res.text.split()
        restext = ''
        for s in restexts:
            restext += ' ' + s

        search_res = []

        hits = re.findall(r'<table class="results">(.*?)</table>', restext, flags=0)
        if len(hits) == 0:
            return f"→ 坏坏诶！猫猫没有找到你说的包！呜呜呜~"
        hits = re.findall(r'<tr>(.*?)</tr>', hits[0], flags=0)
        result = '→ 诶嘿，猫猫找到惹！在下面在下面 ↓\n'
        for i in range(min(5, len(hits))):
            if i == 0:
                continue
            p = re.findall(r'<td.*?</td>', hits[i], flags=0)
            try:
                pkg = {
                    'arch': re.findall(r'<td>(.*?)</td>', p[0], flags=0)[0],
                    'repo': re.findall(r'<td>(.*?)</td>', p[1], flags=0)[0],
                    'name': re.findall(r'">(.*?)</a></td>', p[2], flags=0)[0],
                    'link': baseurl+re.findall(r'href="(.*?)"', p[2], flags=0)[0],
                    'version': re.findall(r'<td>(.*?)</td>', p[3], flags=0)[0],
                    'description': re.findall(r'">(.*?)</td>', p[4], flags=0)[0],
                    'lastupdate': re.findall(r'<td>(.*?)</td>', p[5], flags=0)[0],
                    'flagdate': re.findall(r'<td>(.*?)</td>', p[6], flags=0)[0],
                }
            except Exception:
                pass
            else:
                for k in pkg.keys():
                    inhtmls = re.findall(r'<.*?>', pkg[k], flags=0)
                    for s in inhtmls:
                        pkg[k] = pkg[k].replace(s, '')
                search_res.append(pkg)
        if len(search_res) == 0:
            return f"坏坏诶！猫猫没有找到你说的包！呜呜呜~"
        for rs in search_res:
            result += f"\n" \
                      f"包名:  {rs['name']}\n" \
                      f"版本号:  {rs['version']}\n" \
                      f"架构:  {rs['arch']}\n" \
                      f"软件源:  {rs['repo']}\n"\
                      f"-----------------简介-----------------\n" \
                      f"{rs['description']}\n" \
                      f"--------------------------------------\n" \
                      f"链接:\n{rs['link']}\n"
        return result
    else:
        return '→ 啊咧~是服务器炸了，不关猫猫的事！'


def run(message: Message) -> str:
    req = list(message.raw_message.strip().split(' ', 1))
    helpmsg = ':: Archlinux 包查询(仅官方源)\n' \
              '    .archlinux <packname>'
    if len(req) > 1:
        keywords = req[1].strip()
        return search_arch(keywords)

    return helpmsg


if __name__ == '__main__':
    print(search_arch('linux'))
