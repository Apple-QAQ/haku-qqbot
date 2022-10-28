"""
Arcaea Unlimited Api (AUA)
"""
from typing import Union

import requests

import haku.config

# used for json
true: bool = True
false: bool = False

API = haku.config.Config().get_key('AUA_url')
API = API[0:-1] if API[-1] == "/" else API


class Arcaea:
    def __init__(self, aua_token: str):
        """
        :param aua_token: AUA给予的token
        """
        self.aua_token = aua_token

    def __get(self, url: str, params: dict = None):
        """
        :param url: 请求URL
        :param params: 请求参数
        :return: object()
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/104.0.0.0 Safari/537.36",
            "Authorization": "Bearer " + self.aua_token,
        }

        return requests.get(url=url, headers=headers, params=params, timeout=100)

    def get_all_music_info(self):
        """
        获取所有arc里的歌曲
        :return: 所有arcaea里的歌曲
        """
        get = self.__get(url=f"{API}/song/list")

        if get.status_code != 200:
            return False, get.status_code

        return True, get.json()

    def get_user_info(self, arcaea_id: int):
        """
        获取用户信息
        :param arcaea_id: Arcaea的用户ID
        :return: 用户信息
        """
        _params = {
            "user": arcaea_id,
            "recent": 1,
            "withsonginfo": true,
        }
        get = self.__get(url=f"{API}/user/info", params=_params)

        if get.status_code != 200:
            return False, get.status_code

        return True, get.json()

    def get_user_b30(self, arcaea_id: int):
        """
        获取用户的b30信息
        :param arcaea_id: Arcaea的用户ID
        :return: 用户b30信息
        """
        _params = {
            "usercode": arcaea_id,
            "withrecent": false,
            "overflow": 10,
            "withsonginfo": true,
        }
        get = self.__get(url=f"{API}/user/best30", params=_params)

        if get.status_code != 200:
            return False, get.status_code

        return True, get.json()

    def get_user_best(self, arcaea_id: int, song_name: str, difficulty: int):
        """
        :param arcaea_id: Arcaea的用户id
        :param song_name: 歌曲名字
        :param difficulty: 难度
        :return: 用户最强的歌曲信息
        """
        _params = {
            "user": arcaea_id,
            "songname": song_name,
            "difficulty": difficulty,
            "withsonginfo": true,
        }
        get = self.__get(url=f"{API}/user/best", params=_params)

        if get.status_code != 200:
            return False, get.status_code

        return True, get.json()

    def get_song_random(self, start: Union[str, float], end: Union[str, float]):
        """
        :param start: 开始的
        :param end: 结束的
        :return: 歌曲
        """
        _params = {
            "start": start,
            "end": end,
            "withsonginfo": true,
        }
        get = self.__get(url=f"{API}/song/random", params=_params)

        if get.status_code != 200:
            return False, get.status_code

        return True, get.json()

    def get_song_info(self, song_name: str):
        """
        :param song_name: 歌曲名字
        :return: 歌曲信息
        """
        _params = {
            "songname": song_name,
        }
        get = self.__get(url=f"{API}/song/info", params=_params)

        if get.status_code != 200:
            return False, get.status_code

        return True, get.json()

    def get_song_preview(self, song_name: str, difficulty: int):
        """
        :param song_name: 歌曲名称
        :param difficulty: 歌曲难度
        :return: 歌曲图片
        """
        _params = {
            "songname": song_name,
            "difficulty": difficulty,
        }
        get = self.__get(url=f"{API}/assets/preview", params=_params)

        if get.status_code != 200:
            return False, get.status_code, "https://s2.loli.net/2022/06/18/Fo37uPwOtDzdlMb.jpg"

        return True, None, get.json()
