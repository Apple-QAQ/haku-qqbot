import json
import time
import requests

from handlers.message import Message

url = "http://api.dizhensubao.getui.com/api.htm"


def __time_stamp(time_num):
    time_stamper = float(time_num / 1000)
    time_array = time.localtime(time_stamper)
    other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return other_style_time


def run(message: Message):
    a_day_time = 86400  # a day milliseconds
    start_time = int(round((time.time() - a_day_time) * 1000))  # timestamp 24h before
    dict_1 = {"action": "requestMonitorDataAction", "startTime": start_time, "dataSource": "CEIC"}  # give to the server
    data_json = json.dumps(dict_1)
    res = requests.post(url, data_json, timeout=5)
    earth_json = json.loads(res.text)
    dict_1 = earth_json["values"]  # find  the earthquake

    long_tmp = dict_1[0]['longitude']  # 经度
    lat_tmp = dict_1[0]['latitude']  # 纬度
    # 判断东西南北
    if abs(long_tmp) == long_tmp:
        long_tmp = ["E", str(long_tmp)]
    else:
        long_tmp = ["W", str(-long_tmp)]
    if abs(lat_tmp) == lat_tmp:
        lat_tmp = ["N", str(lat_tmp)]
    else:
        lat_tmp = ["S", str(-lat_tmp)]

    long_tmp[1] = long_tmp[1].split(".")  # 小数点
    long_tmp[1][1] = f"{int(int(long_tmp[1][1]) * 3 / 5)}"  # 分
    lat_tmp[1] = lat_tmp[1].split(".")  # 小数点
    lat_tmp[1][1] = f"{int(int(lat_tmp[1][1]) * 3 / 5)}"  # 分
    long_tmp[1] = f"{long_tmp[1][0]}°{long_tmp[1][1]}'"
    lat_tmp[1] = f"{lat_tmp[1][0]}°{lat_tmp[1][1]}'"
    long_tmp = f"{long_tmp[1]} {long_tmp[0]}"
    lat_tmp = f"{lat_tmp[1]} {lat_tmp[0]}"

    ret = f"→ 最近一次地震的信息\n" \
          f"--------------------------------------\n" \
          f"{dict_1[0]['loc_name']}\n" \
          f"于 {__time_stamp(dict_1[0]['time'])}\n" \
          f"发生了里氏 {dict_1[0]['mag']} 级地震\n" \
          f"-----------INFORMATION------------\n" \
          f"位置信息:\n" \
          f"       {lat_tmp}\n" \
          f"       {long_tmp}\n" \
          f"震源深度:\n" \
          f"       {dict_1[0]['depth'] / 1000}千米\n" \
          f"---------END INFORMATION---------\n" \
          f"检索部分作者: @Billy"

    return ret
