# -*- coding:utf-8 -*-
"""19.1.1 使用动态属性访问JSON数据

"""
from collections import abc
from keyword import iskeyword


class FrozenJSON(object):
    """
    >>> import json
    >>> f = open('data/osconfeed.json', 'r', encoding='utf-8')
    >>> json_data = json.loads(f.read())
    >>> f.close()
    >>> fj = FrozenJSON(json_data)
    >>> len(fj.Schedule.speakers)
    357
    >>> fj.Schedule.speakers[0].name
    'Faisal Abid'
    """

    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self.__data, name):  # 如果name是实例属性__name的属性，返回那个属性，如：调用keys等方法
            return getattr(self.__data, name)
        else:  # 从self.__data中获取name键对应的元素
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(i) for i in obj]
        else:
            return obj


"""FrozenJSON类有一个缺陷：没有对名称为Python关键字的属性做特殊处理。比如name键是：class时。
1.使用keyword.iskeyword(s)判断是否是关键字；
2.使用字符串的isidentifier()方法判断是否是有效的Python标识符。解决：{'2be': 'or not'}

## 类方法build：把嵌套结构转换成FrozenJSON实例或FrozenJSON实例列表。除了在类方法中实现这样的
逻辑，还可以在特殊的__new__方法中实现。
"""


class FrozenJSON2(object):
    """
    >>> import json
    >>> f = open('data/osconfeed.json', 'r', encoding='utf-8')
    >>> json_data = json.loads(f.read())
    >>> f.close()
    >>> fj = FrozenJSON2(json_data)
    >>> len(fj.Schedule.speakers)
    357
    >>> fj.Schedule.speakers[0].name
    'Faisal Abid'
    """

    def __new__(cls, arg):
        """
        特殊方法__new__是个类方法(使用特殊的处理方式，因此不必使用@classmethod装饰器)，必须返回一个实例

        我们几乎不需要自己编写__new__方法，因为从object类继承的实现已经足够了
        """
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(i) for i in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON2(self.__data[name])


"""OSCON的JSON数据有个明显的缺点：索引为40的事件，即名为'There *will* Be Bugs'的那个，
有两位演讲者，3471和5199，但却不容易找到他们。

此外，每条事件记录中都有venue_serial字段，如果想找到对应记录，需要线性搜索Schedule.venues列表
"""


if __name__ == '__main__':
    import doctest

    doctest.testmod()
