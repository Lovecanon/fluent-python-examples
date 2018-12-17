# -*- coding:utf-8 -*-
"""上一份代码会出现`LineItem.weight`报错，原因是描述符类的__get__第一个参数instance为None
我们这里通过类访问托管属性时，最好让__get__方法返回描述符实例
还有一个值得注意的地方：
我们可以把Quantity类放到model模块中。Django模型的字段就是描述符

至此：
Quantity描述符能出色的完成任务。它唯一的缺点是，储存属性的名称是生成的(如：_Quantity#0)，导致用户
难以调试。如果想自动把存储属性的名称设成托管属性的名称需要用到类装饰器和元类。
"""


class Quantity:
    _counter = 0

    def __init__(self):
        """
        `nutmeg._Quantity#0`是无效的Python句法。但使用内置的getattr和setattr函数可以使用这种无效的标识符
        """
        cls = self.__class__
        self.storage_name = '_{}#{}'.format(cls.__name__, cls._counter)
        cls._counter += 1

    def __get__(self, instance, owner):
        """

        :param instance: 托管实例的引用
        :param owner: 托管类的引用，通过描述符从托管类中获取属性时用得到。
        如果使用LineItem.weight从类中获取托管属性(以weight为例)，描述符__get__方法接收到的instance参数
        值是None。LineItem.weight将会抛出异常。
        :return:
        """
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')


class LineItem:
    """

    >>> apple = LineItem('Apple', 10, 9.9)
    >>> apple.subtotal()
    99.0
    >>> getattr(apple, '_Quantity#0')
    10
    >>> getattr(apple, '_Quantity#1')
    9.9
    """

    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    import doctest

    doctest.testmod()
