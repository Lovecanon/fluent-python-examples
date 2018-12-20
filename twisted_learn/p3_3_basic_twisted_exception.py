# -*- coding:utf-8 -*-
"""
尽管我们看到了因第一个回调函数引发异常而出现的跟踪栈，第二个回调函数依然能够执行。
如果你将reactor.stop()注释掉的话，程序会继续运行下去。所以说，reactor并不会因为
回调函数中出现失败（虽然它会报告异常）而停止运行。
"""
from twisted.internet import reactor


def falldown():
    raise Exception('I fall down.')


def upagain():
    print('But I get up again.')
    reactor.stop()


reactor.callWhenRunning(falldown)
reactor.callWhenRunning(upagain)

print('Starting the reactor.')
reactor.run()
