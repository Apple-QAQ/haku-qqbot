# """
# 查询疫情消息
# """
# import requests

# URL = "https://c.m.163.com/ug/api/wuhan/app/data/list-total"  # 网易新冠疫情数据api
# HELP_MSG = ":: 疫情查询:\n" \
#            "    .covid <country> {province||municipality} {city} → 查询疫情"
# HEADERS = {
#     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
#                   "Safari/537.36 Edg/106.0.1370.52",
#     "cookie": "_ntes_nnid=a0dcc49ebf10f6f02be20b685498c549,1665413561959; _ntes_nuid=a0dcc49ebf10f6f02be20b685498c549",
# }


# def __search__(covid_info: dict, search: str) -> bool or dict:
#     """
#     :param covid_info:
#     :param search:
#     :return: 搜索返回数据
#     """
#     for search_things in covid_info:
#         if search in search_things["name"]:
#             return search_things

#     return False


# def __search_return_dict_info__(covid_info: dict or bool) -> dict or bool:
#     """
#     :param covid_info:
#     :return: 疫情数据dict
#     """
#     if type(covid_info) is not dict:
#         return False
#     last_update_time = covid_info["lastUpdateTime"]
#     covid_info = {
#         "today": covid_info['today'],
#         "total": covid_info['total'],
#         "extData": covid_info['extData'],
#     }
#     covid_info_tmp = {
#         "today": {
#             "confirm": "未公布",
#             "suspect": "未公布",
#             "heal": "未公布",
#             "dead": "未公布",
#             "severe": "未公布",
#             "storeConfirm": "未公布",
#             "input": "未公布",
#         },
#         "total": {
#             "confirm": "未公布",
#             "suspect": "未公布",
#             "heal": "未公布",
#             "dead": "未公布",
#             "severe": "未公布",
#             "input": "未公布",
#         },
#         "extData": {
#             "noSymptom": "未公布",
#             "incrNoSymptom": "未公布",
#         },
#     }

#     for key, value in covid_info.items():
#         for key1, value1 in value.items():
#             if value1:
#                 if value1 < 0:
#                     value1 = 0
#             else:
#                 value1 = "未公布"

#             covid_info_tmp[key].update({key1: value1})

#     covid_info = covid_info_tmp

#     today = covid_info['today']  # 今日
#     total = covid_info['total']  # 累积

#     country_covid_info = {
#         "今日": {
#             "境外输入": today['input'],
#             "无症状感染者": covid_info['extData']['incrNoSymptom'],
#             "正在治疗": today['storeConfirm'],
#             "累积确诊": today['confirm'],
#             "死亡": today['dead'],
#             "治愈": today['heal'],
#         },
#         "累积": {
#             "境外输入": total['input'],
#             "无症状感染者": covid_info['extData']['incrNoSymptom'],
#             "正在治疗": int(total['confirm']) - int(total['dead']) - int(total['heal']),
#             "累积确诊": total['confirm'],
#             "死亡": total['dead'],
#             "治愈": total['heal'],
#         },
#         "最后更新日期": last_update_time,
#     }

#     return country_covid_info


# def __return_search_info__(search_info: dict or bool, search_name: str) -> str or bool:
#     """
#     :param search_info:
#     :param search_name:
#     :return:处理过的数据(str)
#     """
#     if type(search_info) is not dict:
#         return False
#     today = search_info["今日"]
#     total = search_info["累积"]
#     # 查询城市数据
#     ret = f"→ 您查询的是 {search_name} 的疫情\n" \
#           f"截止 {search_info['最后更新日期']}\n" \
#           f"------------------------\n" \
#           f"累积境外输入: {total['境外输入']}人 (较昨日 +{today['境外输入']}人)\n" \
#           f"累积无症状: {total['无症状感染者']}人 (较昨日 +{today['无症状感染者']}人)\n" \
#           f"累积治疗: {total['正在治疗']}人 (较昨日 +{today['正在治疗']}人)\n" \
#           f"累积确诊: {total['累积确诊']}人 (较昨日 +{today['累积确诊']}人)\n" \
#           f"累积死亡: {total['死亡']}人 (较昨日 +{today['死亡']}人)\n" \
#           f"累积治愈: {total['治愈']}人 (较昨日 +{today['治愈']}人)"
#     ret = ret.replace("较昨日 +未公布人", "今日数据未公布").replace("未公布人", "未公布")
#     return ret


# def run(message):
#     commands = message.message.split(" ")[1:] if " " in message.message else False  # 用户发送的指令
#     if commands is False:  # 如果 Commands 返回了 False
#         return HELP_MSG

#     covid_info = requests.get(url=URL, timeout=5, headers=HEADERS)  # 疫情数据
#     if covid_info.status_code != 200:
#         return "⇒ 啊哦……api出现了一点问题"
#     else:
#         covid_info = covid_info.json()
#     search_country_info = __search__(covid_info=covid_info["data"]["areaTree"], search=commands[0])  # 查询当国疫情数据

#     if len(commands) == 1:  # 国家
#         search_info = __search_return_dict_info__(covid_info=search_country_info)
#         if search_info is False:
#             return f"⇒ 啊咧……您所查询的国家无相关信息……\n" \
#                    f"{HELP_MSG}"
#         return __return_search_info__(search_info=search_info, search_name=commands[0])
#     else:
#         if commands[0] == "中国":
#             if len(commands) == 2:  # 省
#                 search_info = __search_return_dict_info__(__search__(
#                     covid_info=search_country_info["children"],
#                     search=commands[1]
#                 ))
#                 if search_info is False:
#                     return f"⇒ 喵啊！您所查询的直辖市或省份无相关信息！\n" \
#                            f"{HELP_MSG}"
#                 return __return_search_info__(search_info=search_info, search_name="/ ".join(commands[0:2]))
#             elif len(commands) == 3:  # 市
#                 search_info = __search_return_dict_info__(__search__(
#                     covid_info=search_country_info["children"],
#                     search=commands[1]
#                 ))
#                 if search_info is False:
#                     return f"⇒ 诶多……您所查询的城市或区无相关信息……\n" \
#                            f"{HELP_MSG}"
#                 return __return_search_info__(search_info=search_info, search_name="/".join(commands[0:3]))
#         else:
#             return "⇒ 呜喵……抱歉……除中国外其他国家无法查询城市信息……"

#     return HELP_MSG
