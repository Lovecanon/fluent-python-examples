# -*- coding:utf-8 -*-
"""11.7 定义并使用一个抽象基类

Tombola[tɒmˈbəʊlə] n.纸牌赌博


"""
import abc
import random


class Tombola(abc.ABC):
    """自己定义的抽象基类要继承abc.ABC

    abc.ABC是Python3.4新增的类，如果你是用旧版的Python，那么无法继承现有的抽象基类。
    你必须在class语句中使用`metaclass=abc.ABCMeta`(不是abc.ABC)
    """

    @abc.abstractmethod
    def load(self, iterable):
        """从可迭代对象中添加元素"""

    @abc.abstractmethod
    def pick(self):
        """随机取出一个元素

        如果实例为空，这个方法应该抛出`LookupError`
        """

    def loaded(self):
        """如果至少有一个元素，返回`True`

        **效率不高，子类可以覆盖**
        """
        return bool(self.inspect())

    def inspect(self):
        """返回一个有序元组，由容器现有元素构成，不会修改容器的内容（内部的顺序不保留）

        **效率不高，子类可以覆盖**
        """
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError as e:
                break
        self.load(items)
        return tuple(sorted(items))


"""定义Tombola抽象基类的子类"""


class BingoCage(Tombola):
    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, iterable):
        self._items.extend(iterable)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError as e:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        self.pick()


"""重写耗时的loaded方法和inspect方法。从随机位置上取出一个'数字球'。"""


class LotteryBlower(Tombola):
    """
    >>> blower = LotteryBlower('ABCD')
    >>> blower.load('abcd')
    >>> blower.inspect()
    ('A', 'B', 'C', 'D', 'a', 'b', 'c', 'd')
    >>> blower.loaded()
    True
    >>> picks = [blower.pick() for i in blower.inspect()]
    """


    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LotteryBlower')
        return self._balls.pop(position)

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(sorted(self._balls))

if __name__ == '__main__':
    import doctest
    doctest.testmod()

