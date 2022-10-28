"""
机器人服务器信息
"""
import psutil
import shutil
import time


# api util:
def get_battery() -> dict:
    battery = psutil.sensors_battery()  # 获取电池的信息
    battery_power_connected = battery.power_plugged  # 获取电脑是否连接了电
    battery_power_power = battery.percent  # 获取电池的电量
    return {"power": battery_power_power, "connected": battery_power_connected}


def get_cpu() -> dict:
    cpu = psutil.cpu_count()  # CPU逻辑数量
    cpu_core = psutil.cpu_count(logical=False)  # CPU物理核心
    cpu_percent = psutil.cpu_percent()
    cpu_freq = psutil.cpu_freq().current / 1000  # 频率
    return {"cpu": cpu, "core": cpu_core, "percent": cpu_percent, "freq": cpu_freq}


def get_ram() -> dict:
    ram = psutil.virtual_memory()
    ram_total = ram.total / (1024 ** 3)
    ram_used = ram.used / (1024 ** 3)
    ram_free = ram.free / (1024 ** 3)
    return {"total": ram_total, "used": ram_used, "free": ram_free}


def get_disk() -> dict:
    disk_total, disk_used, disk_free = shutil.disk_usage("/")
    return {"total": disk_total / (1024 ** 3), "used": disk_used / (1024 ** 3), "free": disk_free / (1024 ** 3)}


# return to qq:
def run(message) -> str:
    ping = f"{round((time.time() - message.time) * 1000, 2)} ms"
    meg = message.message.split()[1:]
    ret = " ".join(meg)
    if ret.upper() == "CPU" or ret.upper() == "C":
        return f"# CPU状态:\n" \
               f"    逻辑数量: {get_cpu()['cpu']}\n" \
               f"    物理核心: {get_cpu()['core']}\n" \
               f"    CPU频率: {'%.2f GHz' % get_cpu()['freq']}\n" \
               f"    总使用率: {get_cpu()['percent']}%"

    elif ret.upper() == "RAM" or ret.upper() == "R":
        return f"# RAM信息:\n" \
               f"    所有运存: {'%.2f' % get_ram()['total']} GiB\n" \
               f"    已用运存: {'%.2f' % get_ram()['used']} GiB " \
               f"({'%.2f' % (get_ram()['used'] / get_ram()['total'] * 100)}%)\n" \
               f"    剩余运存: {'%.2f' % get_ram()['free']} GiB " \
               f"({'%.2f' % (get_ram()['free'] / get_ram()['total'] * 100)}%)"

    elif ret.upper() == "DISK" or ret.upper() == 'D':
        return f"# 磁盘信息:\n" \
               f"    磁盘空间: {'%.2f' % get_disk()['total']} GiB\n" \
               f"    已用空间: {'%.2f' % get_disk()['used']} GiB " \
               f"({'%.2f' % (get_disk()['used'] / get_disk()['total'] * 100)}%)\n" \
               f"    剩余空间: {'%.2f' % get_disk()['free']} GiB " \
               f"({'%.2f' % (get_disk()['free'] / get_disk()['total'] * 100)}%)"

    elif ret.upper() == "BATTERY" or ret.upper() == "B":
        try:
            if get_battery()['connected'] is True:
                connected_ret = "正在用电"
            else:
                connected_ret = "正在放电"
            return f"# 电池状态:" \
                   f"    当前电量: {int(get_battery()['power'])}" \
                   f"    电池状态: {connected_ret}"
        except AttributeError:  # 不存在电池
            return "你有电池吗你？"

    elif ret.upper() == "PING" or ret.upper() == "P":
        return f"# 网络:\n" \
               f"   处理时延: {ping}"
    else:
        try:
            if get_battery()['connected'] is True:
                connected_ret = "正在用电"
            else:
                connected_ret = "正在放电"
            ret_battery = f"\n# 电池状态:" \
                          f"    当前电量: {int(get_battery()['power'])}" \
                          f"    电池状态: {connected_ret}"
        except AttributeError:  # 不存在电池
            ret_battery = ""
        return f"让猫猫找找~唔！找到惹！\n" \
               f"# CPU状态:\n" \
               f"    逻辑数量: {get_cpu()['cpu']}\n" \
               f"    物理核心: {get_cpu()['core']}\n" \
               f"    CPU频率: {'%.2f GHz' % get_cpu()['freq']}\n" \
               f"    总使用率: {get_cpu()['percent']}%\n\n" \
               f"# RAM信息:\n" \
               f"    所有运存: {'%.2f' % get_ram()['total']} GiB\n" \
               f"    已用运存: {'%.2f' % get_ram()['used']} GiB " \
               f"({'%.2f' % (get_ram()['used'] / get_ram()['total'] * 100)}%)\n" \
               f"    剩余运存: {'%.2f' % get_ram()['free']} GiB " \
               f"({'%.2f' % (get_ram()['free'] / get_ram()['total'] * 100)}%)\n\n" \
               f"# 磁盘信息:\n" \
               f"    磁盘空间: {'%.2f' % get_disk()['total']} GiB\n" \
               f"    已用空间: {'%.2f' % get_disk()['used']} GiB " \
               f"({'%.2f' % (get_disk()['used'] / get_disk()['total'] * 100)}%)\n" \
               f"    剩余空间: {'%.2f' % get_disk()['free']} GiB " \
               f"({'%.2f' % (get_disk()['free'] / get_disk()['total'] * 100)}%)\n" \
               f"# 网络:\n" \
               f"   处理时延: {ping}" \
               f"{ret_battery}"  # 返回电池，如果没有则ret_battery是空字符串
