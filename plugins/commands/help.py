import time


def run(message) -> str:
    ping = f"{round((time.time() - message.time) * 1000, 2)} ms"
    meg = message.message.split()[1:]
    end = ''
    for i in meg:
        if i == " ":
            pass
        else:
            end += i
    if end != '':
        ret = "猫猫认为.help不需要跟随参数的说~"
    else:
        ret = '''常用指令：
    .help → 你现在在干嘛
    .version → 查看机器人版本
    .music {id} {search} → 网易云音乐
    .loongnews <status> → loongnix.cn 首页新闻
    .archlinux <PackageName> → ArchLinux 包查询
    .arcaea <command> {command} → Arcaea 查询
    .phigros → 获取 Phigros 更新通知
    .debian <PackageName> → Debian 包查询
    .ubuntu <PackageName> → Ubuntu 包查询
    .yiyan <kind> → 一言
    .randompic {loli||pic||picture} → 萝莉好图
    .speak <message> → 让机器人发送消息
    .weather <province||municipality> <city> {day} → 查询天气
    .xiexie → 听我说谢谢你
    .covid <country> {province||municipality} {city} → 查询疫情情况
    .irony <message> → 真·反话
    .morning → 查询群聊问早情况
    .baidu <search> → 拒!绝!伸!手!党!
    .roll <commands> → 投骰子
    .dingzhen → 今天猫猫来到了理塘
    .kemomimi → 每天一只兽耳酱
    .cave {command} {message} → 回声洞
    
-服务器目前时延: %s
-备注：||为或者，<**>为直接替换内容，{**}为根据实际情况选填，不保留"< >"和"{ }"''' % ping

    return ret
    #        .rss <command> {"{link}"} → rss订阅
