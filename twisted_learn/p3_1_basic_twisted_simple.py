# -*- coding:utf-8 -*-

"""
twisted是实现了Reactor模式的，因此它必然会有一个对象来代表这个reactor或者说是事件循环，而这正是twisted的核心。
上面代码的第一行引入了reactor，第二行开始启动事件循环。正常情况下，我们会给出事件循环或文件描述符来监视I/O。

下面我们会让这个程序丰富起来，不过事先要说几个结论：

1.Twisted的reactor只有通过调用reactor.run()来启动。
2.reactor循环是在其开始的进程中运行，也就是运行在主进程中。
3.一旦启动，就会一直运行下去。reactor就会在程序的控制下（或者具体在一个启动它的线程的控制下）。
4.reactor循环并不会消耗任何CPU的资源。
5.并不需要显式的创建reactor实例，只需要引入就OK了

最后一条需要解释清楚。在Twisted中，reactor是Singleton（也是一种模式），即在一个程序中只能有一个reactor，
并且只要你引入它就相应地创建一个

## 有关回调的一些其它说明

1.reactor模式是单线程的。

2.像Twisted这种交互式模型已经实现了reactor循环，意味无需我们亲自去实现它。

3.我们仍然需要框架来调用我们自己的代码来完成业务逻辑。

4.因为在单线程中运行，要想跑我们自己的代码，必须在reactor循环中调用它们。

5.reactor事先并不知道调用我们代码的哪个函数

这样的话，回调并不仅仅是一个可选项，而是游戏规则的一部分。

回调中的几个重要特性：
1.我们的代码与Twisted代码运行在同一个进程中。
2.当我们的代码运行时，Twisted代码是处于暂停状态的。
3.同样，当Twisted代码处于运行状态时，我们的代码处于暂停状态。
4.reactor事件循环会在我们的回调函数返回后恢复运行。


如何从阻塞转换到非阻塞操作取决你具体的操作是什么，但是也有一些Twisted APIs会帮助你实现转换。
值得注意的是，很多标准的Python方法没有办法转换为非阻塞方式。例如，os.system中的很多方法会
在子进程完成前一直处于阻塞状态。这也就是它工作的方式。所以当你使用Twisted时，避开使用os.system。
"""
# from twisted.internet import pollreactor
# pollreactor.install()  # 安装poll，使用poll系统调用代替select

from twisted.internet import reactor
import traceback


def hello():
    print('Hello from the reactor loop!')
    print('Lately I feel like I\'m stuck in a rut.')


def stack():
    print('The python stack:')
    traceback.print_stack()


reactor.callWhenRunning(stack)
print('Starting the reactor.')
reactor.run()
