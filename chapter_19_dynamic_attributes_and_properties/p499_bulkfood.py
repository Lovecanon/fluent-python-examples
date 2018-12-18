# -*- coding:utf-8 -*-
"""19.2 使用特性验证属性
实现特性后，我们可以保持LineItem类的接口保持不变。

通过@prperty和@weight.setter装饰器将weight属性变成特性。

抽象特性的定义有两种方式：使用特性工厂函数、使用描述符类

"""
class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # 初始化设值是会调用 weight.setter 装饰的函数
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')


if __name__ == '__main__':
    li = LineItem('Apple', -9, 10)
