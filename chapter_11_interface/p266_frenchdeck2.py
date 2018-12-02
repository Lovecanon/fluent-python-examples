# -*- coding:utf-8 -*-
"""11.5 定义抽象基类的子类


"""
from collections import MutableSequence
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])


class FrenchDeck(MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suites = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(r, s) for s in self.suites for r in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):
        self._cards[position] = value

    def __delitem__(self, position):
        """继承自`MutableSequence`必须实现`__delitem__`和`insert`方法"""
        del self._cards[position]

    def insert(self, position, value):
        """继承自`MutableSequence`必须实现`__delitem__`和`insert`方法"""
        self._cards.insert(position, value)


if __name__ == '__main__':
    fd = FrenchDeck()
    for i in fd:
        print(i)
