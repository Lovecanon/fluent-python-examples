# -*- coding:utf-8 -*-
from twisted.internet import reactor

class CountDown:
    counter = 5

    def count(self):
        if self.counter == 0:
            reactor.stop()
        else:
            print('counter:{}'.format(self.counter))
            self.counter -= 1
            reactor.callLater(1, self.count)


reactor.callWhenRunning(CountDown().count)
print('Start run')
reactor.run()
print('Stop run')







