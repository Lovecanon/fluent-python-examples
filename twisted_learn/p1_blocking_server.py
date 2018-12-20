# -*- coding:utf-8 -*-
"""

socket.send(string[, flags])
发送TCP数据，返回发送的字节大小。这个字节长度可能少于实际要发送的数据的长度。
换句话说，这个函数执行一次，并不一定能发送完给定的数据，可能需要重复多次才能发送完成。
>>> data = "something you want to send"
>>> while True:
>>>     len = s.send(data[len:])
>>>     if not len:
>>>        break

socket.sendall(string[, flags])
看懂了上面那个，这个函数就容易明白了。发送完整的TCP数据，成功返回None，失败抛出异常
>>> data = "something you want to send"
>>> s.sendall(data)

# TODO 程序运行后Ctrl+C无法关闭程序

# TODO 无法接收客户端发送的数据

# TODO 服务器在服务一个客户端时其它连接进来的客户端只能处于等待状态而得不到服务
"""
import os
import socket
import time
import optparse
import signal


def do_exit(signum, frame):
    print("bye")
    exit()


signal.signal(signal.SIGINT, do_exit)


def parse_args():
    usage = """usage: %prog [options] poetry-file
    This is the Slow Poetry Server, blocking edition.
    Run it like this:
      python slowpoetry.py <path-to-poetry-file>
    If you are in the base directory of the twisted-intro package,
    you could run it like this:
      python blocking-server/slowpoetry.py poetry/ecstasy.txt
    to serve up John Donne's Ecstasy, which I know you want to do.
    """
    parser = optparse.OptionParser(usage)

    parser.add_option('--host',
                      help='The interface to listen on. Default is localhost.',
                      default='localhost')
    parser.add_option('-p', '--port',
                      help='The port to listen on. Default to a random available port.',
                      type='int')
    parser.add_option('-d', '--delay',
                      type='float',
                      help='The number of seconds between sending bytes.',
                      default=.3)
    parser.add_option('-b', '--buffer-size',
                      type='int',
                      help='The number of bytes to send at a time.',
                      default=100)

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error('Provide exactly one poetry file.')
    poetry_file = args[0]
    if not os.path.exists(poetry_file):
        parser.error('No such file:{}'.format(poetry_file))
    return options, poetry_file


def send_poetry(client_socket, poetry_file, buffer_size, delay):
    # receive_buffer = []
    # while True:
    #     data = client_socket.recv(buffer_size)
    #     if not data:
    #         break
    #     receive_buffer.append(data)
    # print('Got data from client:{}'.format(b''.join(receive_buffer)))

    f = open(poetry_file, 'rb')
    while True:
        # 每次服务器都会发送过一行的内容过来。一旦诗歌传送完毕，服务器就会关闭这条连接
        buff = f.read(buffer_size)
        if not buff:
            client_socket.close()
            f.close()
            return
        try:
            client_socket.sendall(buff)
        except socket.error as e:
            client_socket.close()
            f.close()
            return
        time.sleep(delay)


def serve(listen_socket, poetry_file, buffer_size, delay):
    while True:
        client_sock, addr = listen_socket.accept()
        print('Somebody at {} wants poetry!'.format(addr))
        send_poetry(client_sock, poetry_file, buffer_size, delay)


def main():
    options, poetry_file = parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((options.host, options.port or 8000))
    sock.listen(5)

    print('Serving {} on port {}.'.format(poetry_file, sock.getsockname()[1]))
    serve(sock, poetry_file, options.buffer_size, options.delay)


if __name__ == '__main__':
    """可以使用netcat或telnet工具来测试你的服务器"""
    main()
