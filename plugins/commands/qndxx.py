import requests


def run(message):
    commands = message.message.split(" ")[1:]
    first_command = commands[0].upper()

    if first_command == "NEWEST":
        get = requests.get('https://quickso.cn/api/qndxx/api.php', timeout=5).text.replace(' ', ''). \
            replace('</br>', '').replace('\t', '')
        url = f"https://{get}"
        return f"[CQ:image,file={url},cache=0]"
