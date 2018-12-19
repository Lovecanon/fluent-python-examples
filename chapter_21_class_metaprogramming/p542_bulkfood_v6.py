# -*- coding:utf-8 -*-
import doctest
import abc


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        self.storage_name = '_{}#{}'.format(cls.__name__, cls.__counter)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError exception"""


class Quantity(Validated):
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


def entity(cls):
    """1.类装饰器
    此方法是在类组建好了，而且把描述符绑定到类属性上之后，我们通过审查类，为描述符设置合理的
    存储属性名称
    装饰器有个缺点：只对直接依附的类有效。被装饰的类的子类可能继承也可能不继承装饰器所做的改动，具体情况
    视改动的方式而定

    >>> apple = LineItem('apple', 10, 9.9)
    >>> dir(apple)[:3]  # AutoStorage::__set__方法在捣乱
    ['_NonBlank#description', '_Quantity#price', '_Quantity#weight']
    >>> LineItem.description.storage_name
    '_NonBlank#description'
    >>> apple.description  # 走的是描述符的__get__方法
    'apple'

    # self.description = description通过描述符的__set__方法将_NonBlank#description设为apple实例的属性
    >>> getattr(apple, '_NonBlank#description')
    'apple'
    """
    for key, attr in cls.__dict__.items():
        if isinstance(attr, Validated):
            type_name = type(attr).__name__
            attr.storage_name = '_{}#{}'.format(type_name, key)
    return cls


@entity
class LineItem:
    """
    问题：
    `description = NonBlank()` 实例化描述符NonBlank时无法得知托管属性的名称，
    故导致出现储存属性为：_NonBlank#0，而托管属性为：description。这为调试带来极大不便

    解决：
    * 类装饰器
    * 元类
    """

    description = NonBlank()
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price




