# -*- coding:utf-8 -*-
"""方法是描述符


"""
import doctest
from collections import UserString


def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))


class Managed:
    """方法是描述符
    在类中定义的函数属于绑定方法(bound method)，因为用户定义的函数都有__get__方法，所以依附到类上时，就相当于描述符

    >>> obj = Managed()
    >>> obj.spam
    <bound method Managed.spam of <p531_bound_method.Managed object at 0x000001C1959AE208>>
    >>> Managed.spam
    <function Managed.spam at 0x000001AB438F5950>
    >>> obj.spam = 7
    >>> obj.spam
    7

    函数没有实现__set__方法，因此是非覆盖型描述符。obj.spam 和 Managed.spam 获取的是不同的对象。与描述符一样，通过
    托管类访问时，函数的__get__方法会返回自身的引用。但是，通过实例访问时，函数的__get__方法返回的是绑定方法对象：
    一种可调用对象，里面包装着函数，并把托管实例(例如obj)绑定给函数的第一个参数(即self)，这与functools.partial函数
    的行为一致。
    """

    def spam(self):
        print('-> Managed.spam({})'.format(display(self)))


class Text(UserString):
    """
    >>> word = Text('forward')
    >>> word.reverse()
    Text('drawrof')
    >>> Text.reverse.__get__(word)  # 函数都是非覆盖型描述符。在函数上调用__get__方法时传入实例，得到的是绑定到那个实例上的方法
    <bound method Text.reverse of Text('forward')>
    >>> Text.reverse.__get__(None, Text) # 调用函数的__get__方法，如果instance参数的值是None，那么得到的是函数本身
    <function Text.reverse at 0x000001565FB15A60>

    >>> word.reverse.__self__  # 绑定方法对象有个__self__属性，其值是调用这个方法的实例引用
    Text('forward')
    >>> word.reverse.__func__  # 绑定方法的__func__属性是依附在托管类上那个原始函数的引用
    <function Text.reverse at 0x0000025F2D435A60>

    绑定方法对象还有个__call__方法，用于处理真正的调用过程。这个方法会调用__func__属性引用的原始函数，把函数的第一个参数
    设为绑定方法对象的__self__属性。这就是形参self的隐式绑定方式

    函数会变成绑定方法，这是Python语言底层使用描述符最好例证

    """
    def __repr__(self):
        return 'Text({!r})'.format(self.data)

    def reverse(self):
        return self[::-1]
