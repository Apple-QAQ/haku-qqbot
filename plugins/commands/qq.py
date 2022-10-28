import requests

url = "https://zy.xywlapi.cc/qqapi?qq="


def run(message):
    command = message.message.split(" ")[1:]

    if len(command) != 1:
        return f"⇒ 请检查自己的查询方式是否有误，您的输入是 {' '.join(command)} ，但是我们只需要的是数字\n   例如: .qq 10001"

    ret = requests.get(f"{url}{command[0]}", timeout=5).json()
    if ret['status'] == 200:
        return f"您所查询的 QQ id: {ret['qq']}\n" \
               f"QQ 所绑定的电话号: {ret['phone']}\n" \
               f"电话号所在的归属地: {ret['phonediqu']}"
    else:
        import data.log
        data.log.get_logger().info(f"\n{ret}")
        return f"错误: \n" \
               f"status: {ret['status']}"
