# -*- coding:utf-8 -*-
"""不是reactor模式的异步模型客户端

异步模式客户端与同步模式客户端的差别：
1.异步模式客户端一次性与全部服务器完成连接，而不像同步模式那样一次只连接一个。

2.用来进行通信的Socket方法是非阻塞模的，这是通过调用setblocking(0)来实现的。

3.select模块中的select方法是用来识别是其监视的socket是否有完成数据接收的，如果没有它就处于阻塞状态。

4.当从服务器中读取数据时，会尽量多地从Socket读取数据直到它阻塞(EWOULDBLOCK)为止，然后读下一个Socket接收的数据
（如果有数据接收的话）

同步模式客户端也有个循环体（在main函数内），但是这个循环体的每个迭代都是完成一首诗的下载工作。而在异步模式客户端
的每次迭代过程中，我们可以完成所有诗歌的下载或者是它们中的一些。我们并不知道在一个迭代过程中，在下载哪首诗，或者
一次迭代中我们下载了多少数据。这些都依赖于服务器的发送速度与网络环境。我们只需要select函数告诉我们哪个socket有数据
需要接收，然后在保证不阻塞程序的前提下从其读取尽量多的数据。

如果在服务器端口固定的条件下，同步模式的客户端并不需要循环体，只需要顺序罗列三个get_poetry就可以了。但是我们的异步模式
的客户端必须要有一个循环体来保证我们能够同时监视所有的socket端。这样我们就能在一次循环体中处理尽可能多的数据。这个利用
循环体来等待事件发生，然后处理发生的事件的模型非常常见，而被设计成为一个模式：reactor模式。

select模型和其他高效模型：监视一系列sockets（文件描述符）并阻塞程序，直到至少有一个准备好时行I/O操作。

一个真正reactor模式的实现是需要实现循环独立抽象出来并具有如下的功能：

1.监视一系列与I/O操作相关的文件描述符（description)

2.不停地向你汇报哪些准备好I/O操作的文件描述符

一个设计优秀的reactor模式实现需要做到：

1.处理所有不同系统会出现的I/O事件

2.提供优雅的抽象来帮助你在使用reactor时少花些心思去考虑它的存在

3.提供你可以在抽象层外（reactor实现）使用的公共协议实现。

好了，我们上面所说的其实就是Twisted—健壮、跨平台实现了reactor模式并含有很多附加功能。
在第三部分中，实现Twisted版的下载诗歌服务时，我们将开始写一些简单的Twisted程序。

------


### 非阻塞I/O (进程反复调用recvfrom等待返回成功指示)
在网络I/O时候，非阻塞I/O也会进行recvform系统调用，检查数据是否准备好，与阻塞I/O不一样，"非阻塞将大的整片时间的阻塞
分成N多的小的阻塞, 所以进程不断地有机会 '被' CPU光顾"。

也就是说非阻塞的recvform系统调用调用之后，进程并没有被阻塞，内核马上返回给进程，如果数据还没准备好，此时会返回一个
error（EWOULDBLOCK）。进程在返回之后，可以干点别的事情，然后再发起recvform系统调用。重复上面的过程，循环往复的进行
recvform系统调用。这个过程通常被称之为轮询。轮询检查内核数据，直到数据准备好，再拷贝数据到进程，进行数据处理。需要
注意，拷贝数据整个过程，进程仍然是属于阻塞的状态。

"""
import socket
import select
import errno
import optparse
from datetime import datetime


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...
    This is the Get Poetry Now! client, asynchronous edition.
    Run it like this:
      python get-poetry.py port1 port2 port3 ...
    If you are in the base directory of the twisted-intro package,
    you could run it like this:
      python async-client/get-poetry.py 10001 10002 10003
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
    return map(parse_address, address_list)  # map函数返回一个生成器


def get_poetry(sockets):
    sockets = list(sockets)
    poems = dict.fromkeys(sockets, b'')
    sock2task = dict([(s, i) for i, s in enumerate(sockets, start=1)])

    while sockets:
        rlist, _, _ = select.select(sockets, [], [])
        for s in rlist:
            data = b''
            while True:
                try:
                    buff = s.recv(1024)
                except socket.error as e:
                    if e.args[0] == errno.EWOULDBLOCK:
                        # this error code means we would have
                        # blocked if the socket was blocking.
                        # instead we skip to the next socket
                        # 这个错误代码表示如果套接字阻塞我们将阻塞，相反，我们跳到下一个套接字
                        break
                    raise
                else:
                    if not buff:
                        break
                    else:
                        data += buff

            if not data:
                sockets.remove(s)
                s.close()
            else:
                addr_fmt = format_address(s.getpeername())
                msg = 'Task {}: got {} bytes of poetry from {}'.format(sock2task[s], len(data), addr_fmt)
                print(msg)
            poems[s] += data
    return poems


def format_address(address):
    host, port = address
    return '{}:{}'.format(host or '127.0.0.1', port)


def connect(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.setblocking(0)
    return sock


def main():
    address_list = parse_args()
    start = datetime.now()
    sockets = map(connect, address_list)
    poems = get_poetry(sockets)
    elapsed = datetime.now() - start
    for i, sock in enumerate(sockets, start=1):
        print('Task {}:{} bytes of poetry'.format(i, len(poems[sock])))

    print('Got {} poems in {}'.format(len(list(address_list)), elapsed))


if __name__ == '__main__':
    main()
