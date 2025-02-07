"""
sqlite3 数据库处理

用法：
    配置数据库文件目录 : flag = sqlite_set_config(path)
                path 为目录的绝对路径； flag 为是否成功，失败原因可能是不可读写或目标非目录
    判断是否存在数据库 : flag = sqlite_have_db(file)
                file 为文件名或相对路径
    打开数据库 : conn = sqlite_open_db(file)
                conn 为 sqlite3 连接
    提交更改并关闭数据库 : sqlite_close_db(conn)
                会再次调用 conn.commit() 来保证更改的提交
"""
import os
import sqlite3
import sys

__sqlite_path: str


def sqlite_set_config(path: str) -> bool:
    """
    配置 sqlite3 数据库文件路径
    :param path: 绝对路径
    :return: 是否成功
    """
    global __sqlite_path
    __sqlite_path = path
    if os.path.exists(path):
        if not os.path.isdir(path):
            print('冲突的文件：', path, file=sys.stderr)
            return False
        elif not os.access(path, os.R_OK | os.W_OK):
            print('目录不可读写：', path, file=sys.stderr)
            return False
    else:
        os.mkdir(path, 0o755)
    return True


def sqlite_have_db(file: str) -> bool:
    """
    查找是否存在指定 db 文件
    :param file: 文件名/相对路径
    :return: 存在否
    """
    path = os.path.join(__sqlite_path, file)
    return os.path.exists(path)


def sqlite_open_db(file: str) -> sqlite3.Connection:
    """
    读取指定 db 文件
    :param file: 文件名/相对路径
    :return: sqlite3.Connection
    """
    path = os.path.join(__sqlite_path, file)
    conn = sqlite3.connect(path, timeout=20)
    return conn


def sqlite_close_db(conn: sqlite3.Connection):
    """
    提交更改并关闭指定 db 文件
    :param conn: sqlite3 连接
    """
    conn.commit()
    conn.close()
