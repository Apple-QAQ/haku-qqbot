"""
消息处理 Message ，插件命令获取，插件回复消息发送

用法：
    获取实例 : message = Message(message_type, sub_type, message_id, user_id)
              message = Message(message_type, sub_type, message_id, user_id, inter_msg=True)
                inter_msg 用于判断是否为内部消息（用于定时任务消息），默认为聊天消息
    判断是否群消息 : message.is_group_message()
    判断是否临时私聊消息 : message.is_temporary_private_message()
    判断是否为好友私聊消息 : message.is_private_message()
    处理该消息（复读，插件调用） : message.handle()
    发送回复消息（如果有的话） : message.reply_send()

插件调用 Plugin ，具有调用权限黑白名单，支持在线升级

用法：
    获取实例 : plugin = Plugin(name, message)
              plugin = Plugin(name)
              plugin = Plugin()
            name 为插件名，message 为 Message 对象
            message 中至少存在实例化所必须的信息： message_type 、 sub_type 、 message_id 、 user_id ，
            以及 group_id （如果为群消息）、 message 和 raw_message
            注意如果不给出 name 或 message ，则该对象的 handle 方法永远返回 plugin_err_code
    运行插件 : code, msg = plugin.handle()
            将会调用插件的 run() 方法（如果存在），运行前自动进行权限检查，如果不允许调用则获得 plugin_block_code
            code 可能为 plugin_success_code 、 plugin_err_code 或 plugin_block_codd ，msg 为回复的消息
            调用前会先调用 test 方法检查是否存在
    检查插件是否存在 : flag, obj = plugin.test(name)
            flag 为是否存在 True/False ，如果为 True 则 obj 是模块对象
            如果该插件已经载入则调用缓存，反之检查是否存在，存在则载入并写入缓存
            注意每个插件在 bot 整个运行过程中只会被载入一次，首次载入会调用插件的 config() 方法（如果存在）
    重载插件 : plugin.reload()
            首先调用 stop 方法，然后重载所有插件模块，可以用于插件的在线升级
    停止插件 : plugin.stop(dead_lock)
              plugin.stop()
            将会调用插件的 bye() 方法（如果存在）
            dead_lock 参数默认为 False ，如果为 True 则会在之后阻止 reload 方法的调用，这个功能用于在停止时服务使用
"""

import importlib
import re
import threading
import types
from typing import Dict, List, Tuple

import yaml

import api.gocqhttp
import data.json
import data.log
import haku.config
import haku.report
from handlers import message_plugin

plugin_err_code = -1
plugin_success_code = 0
plugin_block_code = 1

_MESSAGE_BLOCK_DEFAULT_CONFIG = {
    "black_group": [],
    "bilibili_catch_black_group": [],
}


def _load_block_default_config():
    try:
        with open("files/block_config.yaml", "r") as config_file:
            return yaml.load(config_file.read(), Loader=yaml.Loader)
    except FileNotFoundError:
        with open("files/block_config.yaml", "x") as config_file:
            yaml.dump(_MESSAGE_BLOCK_DEFAULT_CONFIG, config_file)
            data.log.get_logger().debug("未找到 files/block_config.yaml，完成创建，请根据实际情况填写")
        with open("files/block_config.yaml", "r") as config_file:
            return yaml.load(config_file.read(), Loader=yaml.Loader)


class Message:
    """
    消息类
    """
    # 嗯这些就是为了复读！
    group_msg_cache_1 = {}
    group_msg_cache_2 = {}

    # 特定消息不处理
    __block_msg = [
        '[视频]你的QQ暂不支持查看视频短片，请升级到最新版本后查看。',
    ]

    def __init__(self, message_type: str, sub_type: str, message_id: int, user_id: int, inter_msg: bool = False):
        """
        :param message_type: 消息类型 group private
        :param sub_type: 消息类型 private 时有子类型 group friend
        :param message_id: 消息 id
        :param user_id: 用户 uid
        :param inter_msg: 是否为内部消息 默认为聊天消息
        """
        self.message_type = message_type
        self.sub_type = sub_type
        self.message_id = message_id
        self.user_id = user_id
        self.group_id = 0
        self.self_id = 0
        self.message = self.raw_message = ''
        self.time = 0
        self.info: dict
        self.reply: str = ''
        # 调用 handle 以后可以检查是否调用了插件
        self.can_call = False
        # 内部消息 即不是聊天消息
        self.inter_msg = inter_msg

    def is_group_message(self):
        return self.message_type == 'group'

    def is_private_message(self):
        return self.message_type == 'private' and self.sub_type == 'friend'

    def is_temporary_private_message(self):
        return self.message_type == 'private' and self.sub_type == 'group'

    def handle(self):
        """
        处理消息 判断插件调用 获取插件回复
        """
        if self.message in self.__block_msg:
            return

        if not self.inter_msg:
            # 判断是否调用插件
            load_block_default_config = _load_block_default_config()
            black_group = load_block_default_config["black_group"]
            data.log.get_logger().info(f"black_group: {black_group}")

            # 判断是否调用插件
            call_plugin = False
            plugin_name = ''
            try:
                index = haku.config.Config().get_index()
                message_sequence = self.message.split()
                plugin_name_judge = r'^[_A-Za-z]+$'.format(index)
                if len(message_sequence) <= 0 or len(message_sequence[0]) <= 0:
                    return
                com = re.compile(plugin_name_judge)
                index_len = len(index)
                if com.match(message_sequence[0][index_len:]) is not None and message_sequence[0][:index_len] == index:
                    plugin_name = message_sequence[0][1:]
                    call_plugin = True
            except Exception as e:
                data.log.get_logger().exception(f'RuntimeError while checking message: {e}')

            # 调用插件
            if call_plugin:
                self.can_call = True
                plugin = Plugin(plugin_name, self)
                code, self.reply = plugin.handle()
            else:
                # 信息处理插件 handlers/message_plugin.py
                message_plugin.plugins(self=self, block_default_config=load_block_default_config)

    def reply_send(self):
        """
        发送回复消息
        :return:
        """
        try:
            if len(self.reply) <= 0:
                return
        except TypeError:
            pass
        if self.is_group_message():
            api.gocqhttp.send_group_msg(self.group_id, self.reply)
        elif self.is_private_message():
            api.gocqhttp.send_private_msg(self.user_id, self.reply)
        elif self.is_temporary_private_message():
            api.gocqhttp.send_temporary_private_msg(self.user_id, self.group_id, self.reply)


class Plugin:
    """
    插件类
    插件首次载入配置： config()
    插件调用： run(Message) -> str
    插件退出： bye()
    """
    __plugin_prefix = 'plugins.commands.'
    __plugin_default_config = {
        'blacklist': {'group_id': [], 'user_id': []},
        'whitelist': {'group_id': [], 'user_id': []},
    }
    __plugin_object_dict: Dict[str, Tuple[bool, types.ModuleType]] = {}
    __plugin_reload_lock = threading.Lock()

    def __init__(self, name: str = '', message: Message = None):
        self.plugin_name = name.strip()
        self.message = message

    def __authorized(self, plugin_name: str) -> bool:
        """
        准入黑白名单 先判断黑名单后判断白名单
        :param plugin_name: 插件名
        :return: 是否可以运行
        """
        file = f'{plugin_name}.json'
        if data.json.json_have_file(file):
            my_config = data.json.json_load_file(file)
            allow = True
            try:
                white = my_config['whitelist']
                black = my_config['blacklist']
                group = black['group_id']
                user = black['user_id']
                if len(group) > 0 or len(user) > 0:
                    if self.message.is_group_message() and \
                            (self.message.group_id in group or self.message.user_id in user):
                        allow = False
                    elif self.message.is_private_message() and self.message.user_id in user:
                        allow = False
                group = white['group_id']
                user = white['user_id']
                if allow and (len(group) > 0 or len(user) > 0):
                    allow = False
                    if self.message.is_group_message() and \
                            (self.message.group_id in group or self.message.user_id in user):
                        allow = True
                    elif self.message.is_private_message() and self.message.user_id in user:
                        allow = True
                return allow
            except Exception as e:
                data.log.get_logger().exception(f'RuntimeError while authorizing plugin {plugin_name}: {e}')
                return False
        else:
            data.json.json_write_file(file, self.__plugin_default_config)
        return True

    def handle(self) -> (int, str):
        """
        调用插件并返回回复消息
        :return: 操作代码(plugin_success_code/plugin_err_code/plugin_block_code), 回复消息
        """
        if self.plugin_name is None or len(self.plugin_name) <= 0 or self.message is None:
            return plugin_err_code, ''
        return_code = plugin_success_code
        plugin_name = self.__plugin_prefix + self.plugin_name
        plugin_message = ''

        # 载入判断
        flag, cfg_flag, plugin_obj = self.test(self.plugin_name)
        if flag:
            # 权限检查
            if self.__authorized(plugin_name):
                if cfg_flag:
                    # 运行 run()
                    if 'run' in dir(plugin_obj):
                        try:
                            plugin_message = plugin_obj.run(self.message)
                        except Exception as e:
                            data.log.get_logger().exception(f'RuntimeError while running module {plugin_name}: {e}')
                else:
                    plugin_message = '模块载入错误 (ᗜ˰ᗜ)'
            else:
                return_code = plugin_block_code
                data.log.get_logger().debug(
                    f'The plugin request from group {self.message.group_id} '
                    f'user {self.message.user_id} was blocked'
                )
        else:
            return_code = plugin_err_code

        return return_code, plugin_message

    def test(self, plugin_name: str = None) -> (bool, bool, object):
        """
        测试是否存在插件，存在则载入并配置
        :param plugin_name: 插件名
        :return: 是否成功载入，是否成功配置，模块对象
        """
        # 模块名
        if plugin_name is None:
            module_name = self.__plugin_prefix + self.plugin_name
        else:
            module_name = self.__plugin_prefix + plugin_name

        # 载入插件
        data.log.get_logger().debug(f'Now test plugin {module_name}')
        plugin_obj = self.__plugin_object_dict.get(module_name)
        if plugin_obj is None:
            try:
                plugin_obj = importlib.import_module(module_name)
            except ModuleNotFoundError:
                data.log.get_logger().debug(f'No such plugin {module_name}')
                return False, False, None
            else:
                cfg_flag = True
                # 运行 config()
                if 'config' in dir(plugin_obj):
                    try:
                        plugin_obj.config()
                    except Exception as e:
                        data.log.get_logger().exception(f'RuntimeError while configuring module {module_name}: {e}')
                        cfg_flag = False
                # 记入缓存
                self.__plugin_object_dict.update({module_name: (cfg_flag, plugin_obj)})
                return True, cfg_flag, plugin_obj
        return True, plugin_obj[0], plugin_obj[1]

    def reload(self):
        """
        插件重载
        """
        with self.__plugin_reload_lock:
            delete_name: List[str] = []
            self.stop()
            for name, obj in self.__plugin_object_dict.items():
                try:
                    new_obj = importlib.reload(obj[1])
                    # 运行 config()
                    cfg_flag = True
                    if 'config' in dir(new_obj):
                        try:
                            new_obj.config()
                        except Exception as e:
                            data.log.get_logger().exception(f'RuntimeError while reconfiguring module {name}: {e}')
                            cfg_flag = False
                    self.__plugin_object_dict[name] = (cfg_flag, new_obj)
                except ModuleNotFoundError:
                    # 插件已经不存在
                    delete_name.append(name)
                except Exception as e:
                    error_msg = f'RuntimeError while reload module {name}: {e}'
                    data.log.get_logger().exception(error_msg)
                    haku.report.report_send(error_msg)
            for name in delete_name:
                self.__plugin_object_dict.pop(name)

    def stop(self, dead_lock: bool = False):
        """
        插件退出
        :param dead_lock: 之后不再允许插件重载（停止服务时置为 True）
        """
        if dead_lock:
            if not self.__plugin_reload_lock.locked():
                self.__plugin_reload_lock.acquire()
        for obj in self.__plugin_object_dict.values():
            if 'bye' in dir(obj):
                try:
                    obj.bye()
                except Exception as e:
                    data.log.get_logger().exception(f'RuntimeError while quit module {obj.__name__}: {e}')
