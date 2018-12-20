# -*- coding:utf-8 -*-
"""
poem [ˈpəʊɪm] n.诗;韵文;诗一样的作品;富有诗意的东西
“诗”，为可数名词，可指具体的一首诗、两首诗、几首诗等；用作主语时，谓语动词的数取决于poem的数

poetry [ˈpəʊətri] n.诗，诗歌;诗意，诗情;作诗;诗歌艺术
“诗”，但为诗的总称，是不可数名词；用作主语时，谓语动词总是用单数

`E:\workbench\fluent-python-examples\twisted_learn>python p1_blocking_client.py 8000 8001 8002`
由于这个客户端采用的是阻塞模式，因此它会一首一首的下载，即只有在完成一首时才会开始下载另外一首

"""
import socket
import optparse
from datetime import timedelta
from datetime import datetime


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...
    This is the Get Poetry Now! client, blocking edition.
    Run it like this:
      python get-poetry.py port1 port2 port3 ...
    If you are in the base directory of the twisted-intro package,
    you could run it like this:
      python blocking-client/get-poetry.py 10001 10002 10003
    to grab poetry from servers on ports 10001, 10002, and 10003.
    Of course, there need to be servers listening on those ports
    for that to work.
    """
    parser = optparse.OptionParser(usage)
    _, address_list = parser.parse_args()
    if not address_list:
        print(parser.format_help())
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)
        if not port.isdigit():
            parser.error('Ports must be integers.')
        return host, int(port)

    return map(parse_address, address_list)


def get_poetry(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    poem = b''
    while True:
        buff = sock.recv(1024)
        if not buff:
            sock.close()
            break
        poem += buff
    return poem


def format_address(address):
    host, port = address
    return '{}:{}'.format(host or '127.0.0.1', port)


def main():
    address_list = parse_args()
    total_elapsed = timedelta()
    for i, address in enumerate(address_list, start=1):
        addr_fmt = format_address(address)
        print('Task {}: got poetry from:{}'.format(i, addr_fmt))
        start = datetime.now()
        poem = get_poetry(address)
        elapsed = datetime.now() - start
        msg = 'Task {}: got {} bytes of poetry from {} in {}'.format(i, len(poem), addr_fmt, elapsed)
        print(msg)
        total_elapsed += elapsed
    print('Got {} poems in {}'.format(i, total_elapsed))



if __name__ == '__main__':
    main()
