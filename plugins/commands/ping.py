"""
ping
TODO: ping ip
"""
import data.log


def config():
    data.log.get_logger().debug('run ping.config()')


def run(message) -> str:
    meg = message.message.split()[1:]
    end = ''
    for i in meg:
        if i == " ":
            pass
        else:
            end += i
    if end != '':
        return '猫猫认为.ping不需要跟随参数的说~'
    else:
        data.log.get_logger().debug('run ping.run(message)')
        return 'pong!'


def bye():
    data.log.get_logger().debug('run ping.quit()')
