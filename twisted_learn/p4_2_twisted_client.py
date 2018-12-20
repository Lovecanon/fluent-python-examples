# This is the Twisted Get Poetry Now! client, version 1.0.
"""
NOTE: This should not be used as the basis for production code.
It uses low-level Twisted APIs as a learning exercise.

我们开始学习使用Twisted时会使用一些低层Twisted的APIs。这样做是为揭去Twisted的抽象层，这样我们就可以从内向外的来
学习Twisted。记住一点就行：这些代码只是用作练习，而不是写真实软件的例子。

"""
import datetime, errno, optparse, socket

from twisted.internet import main
from twisted.internet import reactor


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...
        This is the Get Poetry Now! client, Twisted version 1.0.
        Run it like this:
          python get-poetry.py port1 port2 port3 ...
        If you are in the base directory of the twisted-intro package,
        you could run it like this:
          python twisted-client-1/get-poetry.py 10001 10002 10003
        to grab poetry from servers on ports 10001, 10002, and 10003.
        Of course, there need to be servers listening on those ports
        for that to work.
        """
    parser = optparse.OptionParser(usage)
    _, addresses = parser.parse_args()
    if not addresses:
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

    return list(map(parse_address, addresses))


class PoetrySocket(object):
    poem = b''

    def __init__(self, task_num, address):
        self.task_num = task_num
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(address)
        self.sock.setblocking(0)

        # tell the Twisted reactor to monitor this socket for reading
        reactor.addReader(self)

    def fileno(self):
        """IReadDescriptor是IFileDescriptor的一个子类"""
        try:
            return self.sock.fileno()
        except socket.error:
            return -1

    def connectionLost(self, reason):
        """IReadDescriptor是IFileDescriptor的一个子类"""
        self.sock.close()

        # stop monitoring this socket
        from twisted.internet import reactor
        reactor.removeReader(self)

        # see if there are any poetry sockets left
        for reader in reactor.getReaders():
            if isinstance(reader, PoetrySocket):
                return
        reactor.stop()  # no more poetry

    def doRead(self):
        """
        此方法被Twisted的reactor调用时，就会采用异步的方式从socket中读取数据。
        doRead其实就是一个回调函数，只是没有直接将其传递给reactor，而是传递一个实现此方法的对象实例。
        这也是Twisted框架中的惯例——不是直接传递实现某个接口的函数而是传递实现它的对象。这样我们通过一个
        对象参数就可以传递一组相关的回调函数。而且也可以让回调函数之间通过存储在对象中的数据进行通信。
        """
        data = b''
        while True:
            try:
                buff = self.sock.recv(1024)
                if not buff:
                    break
                else:
                    data += buff
            except socket.error as e:
                if e.args[0] == errno.EWOULDBLOCK:
                    break
                return main.CONNECTION_LOST

        if not data:
            print('Task %d finished' % self.task_num)
            return main.CONNECTION_DONE
        else:
            msg = 'Task %d: got %d bytes of poetry from %s'
            print(msg % (self.task_num, len(data), self.format_addr()))
        self.poem += data

    def logPrefix(self):
        """IFileDescriptor继承了ILooggingContext"""
        return 'poetry'

    def format_addr(self):
        host, port = self.address
        return '%s:%s' % (host or '127.0.0.1', port)


def poetry_main():
    addresses = parse_args()
    start = datetime.datetime.now()
    sockets = [PoetrySocket(i, addr) for i, addr in enumerate(addresses, start=1)]
    reactor.run()
    elapsed = datetime.datetime.now() - start
    for i, sock in enumerate(sockets):
        print('Task %d: %d bytes of poetry' % (i + 1, len(sock.poem)))
    print('Got %d poems in %s' % (len(addresses), elapsed))


if __name__ == '__main__':
    poetry_main()
