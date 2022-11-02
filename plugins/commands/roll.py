"""
骰子(随机数)
"""

import re
from random import randint

import data.log

help_msg = ":: 投骰子\n" \
           "    .roll <from>,<to> → 投骰子(从 from 到 to 的范围中选一个随机数)\n" \
           "    .roll r<times>d<to> → 跑团"


def run(message):
    try:
        commands = message.message.split(" ", 1)

        if len(commands) != 2:
            return "⇒ 使用方式错误啦baka！请使用 .roll help 查看教程喵！"
        elif commands[1].upper() == "HELP":
            return help_msg

        if "," in commands[1]:
            randint_from = int(commands[1].split(",")[0])
            randint_to = int(commands[1].split(",")[-1])

            return f"→ 您的骰子点数是从 {randint_from} 到 {randint_to}\n" \
                   f"结果为: {randint(randint_from, randint_to)}"
        elif "r" in commands[1] and "d" in commands[1]:
            x = int(re.search(r'r(\d*)', commands[1]).group()[1:])
            y = int(re.search(r'd(\d*)', commands[1]).group()[1:])

            if not 1 <= x <= 10:
                return f"⇒ r 应该控制在 1 ≤ r ≤ 10 内! 当前的 r 是 {x}。"

            acc = 0

            for i in range(x):
                acc += randint(1, y)

            return f"→ 您的骰子点数是从 1 到 {y}, 循环了 {x} 次\n" \
                   f"结果为: {acc}"

    except Exception as e:
        data.log.get_logger().error(e)
        return help_msg
