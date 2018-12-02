# -*- coding:utf-8 -*-
"""

"""
from random import shuffle
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])


class FrenchDeck(object):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suites = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(r, s) for s in self.suites for r in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


"""
以上`FrenchDeck`类最大的缺陷是不能洗牌，即`FrenchDeck`类只实现了不可变的序列协议；
可变的序列协议必须提供`__setitem__`方法；
shuffle方法必须传入一个可变序列。
"""


def set_card(deck, position, card):
    """Monkey patch

    >>> FrenchDeck.__setitem__ = set_card
    >>> deck = FrenchDeck()
    >>> shuffle(deck)
    >>> len(deck)
    52
    """
    deck._cards[position] = card


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)