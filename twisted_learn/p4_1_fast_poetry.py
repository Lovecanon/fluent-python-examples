# -*- coding:utf-8 -*-
# This is the Twisted Fast Poetry Server, version 1.0

import optparse, os

from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import reactor


def parse_args():
    usage = """usage: %prog [options] poetry-file
            This is the Fast Poetry Server, Twisted edition.
            Run it like this:
              python fastpoetry.py <path-to-poetry-file>
            If you are in the base directory of the twisted-intro package,
            you could run it like this:
              python twisted-server-1/fastpoetry.py poetry/ecstasy.txt
            to serve up John Donne's Ecstasy, which I know you want to do.
            """

    parser = optparse.OptionParser(usage)
    h = "The interface to listen on. Default is localhost."
    parser.add_option('--host', help=h, default='localhost')
    h = "The port to listen on. Default to a random available port."
    parser.add_option('--port', type='int', help=h)

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error('Provide exactly one poetry file.')

    poetry_file = args[0]
    if not os.path.exists(args[0]):
        parser.error('No such file: %s' % poetry_file)
    return options, poetry_file


class PoetryProtocol(Protocol):

    def connectionMade(self):
        self.transport.write(self.factory.poem)
        self.transport.loseConnection()


class PoetryFactory(ServerFactory):
    protocol = PoetryProtocol

    def __init__(self, poem):
        self.poem = poem


def main():
    options, poetry_file = parse_args()

    f = open(poetry_file, 'rb')
    poem = f.read()
    f.close()

    factory = PoetryFactory(poem)
    port = reactor.listenTCP(options.port, factory, interface=options.host)
    print('Serving %s on %s.' % (poetry_file, port.getHost()))
    reactor.run()


if __name__ == '__main__':
    main()
