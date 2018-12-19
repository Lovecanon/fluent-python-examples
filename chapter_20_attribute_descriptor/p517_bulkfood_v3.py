# -*- coding:utf-8 -*-
"""属性描述符
描述符是对多个属性运用相同存取逻辑的一种方式。

"""

"""描述符
实现__get__,  __set__或__delete__方法的类是描述符。
描述符用法：创建一个实例，作为另一个类的类属性

描述符类：实现描述符协议的类。如：Quantity类
托管类：把描述符实例声明为类属性的类。如：LineItem类
描述符实例：描述符类的各个实例，声明为托管类的类属性
托管实例：托管类的实例。如：LineItem实例是托管实例
* 存储属性：*托管实例*中存储*自身托管属性*的属性。如：LineItem实例的weight和price属性是存储属性
* 托管属性：*托管类*中由描述符实例处理的公开属性，值存储在存储属性中

Quantity实例是LineItem类的类属性，这一点一定要理解。

"""


class Quantity:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        """
        这里，必须直接处理托管实例的__dict__属性；如果使用内置的setattr函数，会再次触发__set__方法，导致无限递归
        :param instance: 托管实例
        :param value: 要设定的值
        :return:
        """
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')


class LineItem3:
    """
    >>> l = LineItem3('Apple', 10, 9.9)
    >>> l.subtotal()
    99.0

    """
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    import doctest

    doctest.testmod()

