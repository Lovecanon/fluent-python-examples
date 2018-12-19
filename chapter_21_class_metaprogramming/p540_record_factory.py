# -*- coding:utf-8 -*-


def record_factory(cls_name, field_names):
    """类工厂函数
    其中有个缺陷，不能序列化

    collections.nametuple之所以使用模板和exec函数来创建类，是因为之后可以通过_source属性访问类代码
    """
    try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError as e:
        pass
    field_names = tuple(field_names)

    def __init__(self, *args, **kwargs):
        attrs = dict(zip(field_names, args))
        attrs.update(kwargs)
        for k, v in attrs.items():
            setattr(self, k, v)

    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(
        __slots__=field_names,
        __init__=__init__,
        __iter__=__iter__,
        __repr__=__repr__
    )
    return type(cls_name, (object,), cls_attrs)


if __name__ == '__main__':
    Student = record_factory('Student', 'name age')
    jack = Student('Jack', 12)
    print(jack)
