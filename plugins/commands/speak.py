import html


def run(message):
    meg = message.message.split(" ")[1:]
    ret = html.unescape(" ".join(meg))
    return ret
