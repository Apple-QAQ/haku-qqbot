"""
查询天气（和风天气api）
"""
import json

import requests

import data.log
import haku.config
from handlers.message import Message

HEKEY = haku.config.Config().get_key('hefeng_weather')


def run(message: Message):
    KEY = HEKEY  # 和风天气key
    if KEY:
        helpMsg = ':: 查询天气~\n' \
                  '  .weather <城市> <地区> {n日后}\n' \
                  '  0(今天) ≥ n ≥ 2(2日后)\n\n' \
                  '→ 感谢和风提供的api和@白狐狐！'
        req = list(message.message.split())
        for i in range(0, len(req)):
            req[i] = req[i].strip()
        # else:
        url1 = 'https://geoapi.heweather.net/v2/city/lookup'
        url2 = 'https://devapi.heweather.net/v7/weather/3d'
        ans = ''
        params = {'key': KEY}
        try:
            days = int(req[3])
        except:
            days = 100
        try:
            params.update({'location': req[2], 'adm': req[1]})
        except:
            return helpMsg
        try:
            resp = requests.get(url=url1, params=params, timeout=5)
            if resp.status_code == 200:
                try:
                    rejson = json.loads(resp.text)
                    data.log.get_logger().debug(rejson)
                    cityId = rejson['location'][0]['id']
                    province = rejson['location'][0]['adm1']
                    city = rejson['location'][0]['adm2']
                    resp = requests.get(url=url2, params={'key': KEY, 'location': cityId}, timeout=5)
                except KeyError:
                    return helpMsg
                if resp.status_code == 200:
                    if 0 <= days <= 2 and len(req) == 4 and (days == 0 or days == 1 or days == 2):
                        rejson = json.loads(resp.text)
                        data.log.get_logger().debug(rejson)
                        ans = f"地区: {province} - {city}\n" \
                              f"日期: {rejson['daily'][days]['fxDate']}\n" \
                              f"-----------------------\n" \
                              f"天气: {rejson['daily'][days]['textDay']}\n" \
                              f"气温: {rejson['daily'][days]['tempMin']}~{rejson['daily'][days]['tempMax']} ℃\n" \
                              f"风向: {rejson['daily'][days]['windDirDay']}\n" \
                              f"风力: {rejson['daily'][days]['windScaleDay']} 级\n" \
                              f"风速: {rejson['daily'][days]['windSpeedDay']} km/h\n" \
                              f"气压:{rejson['daily'][days]['pressure']} hPa"
                    elif days == 100:
                        try:
                            rejson = json.loads(resp.text)
                            data.log.get_logger().debug(rejson)
                            ans = f"地区: {province} - {city}\n" \
                                  f"\n------------------------------"
                            for n in range(3):
                                ans += f"\n" \
                                       f"日期: {rejson['daily'][n]['fxDate']}\n" \
                                       f"------------{n}天后------------\n" \
                                       f"天气: {rejson['daily'][n]['textDay']}\n" \
                                       f"气温: {rejson['daily'][n]['tempMin']}~{rejson['daily'][n]['tempMax']} ℃\n" \
                                       f"风向: {rejson['daily'][n]['windDirDay']}\n" \
                                       f"风力: {rejson['daily'][n]['windScaleDay']} 级\n" \
                                       f"风速: {rejson['daily'][n]['windSpeedDay']} km/h\n" \
                                       f"气压:{rejson['daily'][n]['pressure']} hPa\n" \
                                       f"------------------------------"
                        except KeyError:
                            return helpMsg
                else:
                    ans = '好像返回了奇怪的东西: ' + str(resp.status_code)
            elif resp.status_code == 404:
                ans = '真的有这个地方咩，别骗猫猫！'
            else:
                ans = '好像返回了奇怪的东西: ' + str(resp.status_code)
        except Exception as e:
            data.log.get_logger().exception(f'RuntimeError in plugin forecast: {e}')
            ans = '啊嘞嘞好像出错了，一定是和风炸了不关猫猫的事情(溜走)'
    else:
        ans = '好像和风不让查诶...'
    return ans
