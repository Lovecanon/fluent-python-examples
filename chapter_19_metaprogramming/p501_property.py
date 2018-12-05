# -*- coding:utf-8 -*-
"""
python 查看对象属性相关方法：__dict__, dir(), vars(), locals()

object.__dict__一般是字典或其他映射对象，用来存储一个对象(可写的)的属性。

* 内建类型对象中是不存在这个属性的，内建对象访问会出现AttributeError错误。
* 类对象的Class.__dict__只返回当前类的属性字典，但不包含其基类的属性。
dir(Class)会返回当前类以及它的所有基类的类属性名，即当前类及所有基类的__dict__键值。
* 实例对象的obj.__dict__返回实例对象绑定的属性字典。dir(obj)会返回实例属性和构造类以及所有基类的属性列表。
# >>> Foo.__dict__
# {'__module__': '__main__', '__doc__': "\n    >>> foo = Foo()\n    >>> vars(foo)  # vars() 函数返回对象object的属性和属性值的字典对象。\n    {}\n    >>> foo.data\n    'the class attribute: data'\n    >>> foo.__dict__\n    {}\n\n    ", 'data': 'the class attribute: data', 'prop': <property object at 0x000002889BD88778>, '__dict__': <attribute '__dict__' of 'Foo' objects>, '__weakref__': <attribute '__weakref__' of 'Foo' objects>}
>>> # Foo.__dict__.keys()：['__module__', '__doc__', 'data', 'prop', '__dict__', '__weakref__']
>>> dir(Foo)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'data', 'prop']

>>> foo = Foo()
>>> foo.__dict__
{}
>>> dir(foo)  # 包含类属性data和特性prop
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'data', 'prop']


1).dir() 不带参数时，返回当前范围内名称**列表**。和locals()，vars()不带参数类似，后面返回的是字典。
2).dir(module) 作用于模块时，返回模块的属性列表。即模块struct.__dict__的键值列表。
3).当dir(obj)作用于实例对象，且它的构造类或基类有__dir__方法，dir(obj)返回自定义的列表内容。
4).当dir(obj)作用于实例对象，且它的构造类或基类没有__dir__方法，则dir(obj)返回obj的实例属性，还有构造类及基类的类属性。
5).当dir(class作用于类对象，返回当前类及所有基类的类属性列表。


vars([object])就是返回对象__dict__的内容，无论是类对象还是实例对象，vars([object]) == object.__dict__。
当然，参数对象需要有一个__dict__属性。同样的，内建对象没有__dict__属性会报TypeError错误。


locals()返回调用者当前局部名称空间的字典。在一个函数内部，局部名称空间代表在函数执行时候定义的所有名字，
locals()函数返回的就是包含这些名字的字典。


"""


class Foo:
    """
    >>> foo = Foo()
    >>> vars(foo)  # vars() 函数返回对象object的属性和属性值的字典对象。
    {}
    >>> foo.data
    'the class attribute: data'
    >>> foo.__dict__
    {}

    >>> foo.data
    'the class attribute: data'
    >>> foo.data = 'custom data'
    >>> vars(foo)
    {'data': 'custom data'}

    # >>> foo.prop = 'custom prop'  # 不能设置实例属性，报错！！！
    >>> foo.__dict__['prop'] = 'custom prop'
    >>> foo.prop  # 实例属性会覆盖类属性，但特性没被实例属性遮盖
    'the prop value'
    >>> vars(foo)
    {'data': 'custom data', 'prop': 'custom prop'}

    >>> Foo.prop = 'a'  # 覆盖Foo.prop特性，销毁特性对象
    >>> foo.prop
    'custom prop'
    """
    data = 'the class attribute: data'

    @property
    def prop(self):
        return 'the prop value'


if __name__ == '__main__':
    import doctest
    doctest.testmod()