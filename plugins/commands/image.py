def run(message):
    url = " ".join(message.message.split(" ")[1:])
    return f"[CQ:image,file={url},cache=0]"
