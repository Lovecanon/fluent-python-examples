# -*- coding:utf-8 -*-
"""覆盖型和非覆盖型描述符的差别：
叫法差别：覆盖型描述符也叫数据描述符或强制描述符
          非覆盖型描述符也叫非数据描述符或遮盖型描述符

语法差别：非覆盖型描述符是描述符中没有定义__set__方法
用法差别：非覆盖型描述符中`obj.non_over = 7`赋值方式能轻松*遮盖*Managed类的同名描述符属性

覆盖型的理解：因为描述符中定义了__set__方法，对实例属性进行赋值obj.over = 7后，再获取obj.over属性还是描述符，*覆盖*
了对实例属性的赋值。

非覆盖型描述符的理解：没有定义__set__方法，对实例属性进行赋值obj.non_over = 7后，再获取obj.over属性将得到 7，即使定义了
__get__方法也没有走。

一句话总结：描述符会不会覆盖实例属性；反过来说，实例属性会不会遮盖描述符
"""
# import doctest
#
# doctest.testmod()


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


def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


class Overriding:
    """覆盖型描述符
    实现__set__方法的描述符属于覆盖型描述符，因为虽然描述符是类属性，但是实现__set__方法的话，
    会覆盖对实例属性的赋值操作

    特性(property)也是覆盖型描述符
    >>> obj = Managed()
    >>> obj.over
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> Managed.over
    -> Overriding.__get__(<Overriding object>, None, <class Managed>)
    >>> obj.over = 7  # 为obj.over赋值，触发描述符的__set__方法，最后一个参数是7
    -> Overriding.__set__(<Overriding object>, <Managed object>, 7)
    >>> obj.over
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)

    >>> obj.__dict__['over'] = 8
    >>> vars(obj)
    {'over': 8}
    >>> obj.over  # 即使名为over的实例属性, Managed.over描述符仍会覆盖读取 obj.over 这个操作
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    """

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:
    """没有__get__方法的覆盖型描述符

    >>> obj = Managed()
    >>> obj.over_no_get  # 这个覆盖型描述符没有__get__方法，因此，obj.over_no_get从类中获取描述符实例
    <p527_descriptor_kinds.OverridingNoGet object at 0x000001A1E9CA8B00>
    >>> Managed.over_no_get  # 直接从托管类中读取描述符实例
    <p527_descriptor_kinds.OverridingNoGet object at 0x0000020C78058978>

    >>> obj.over_no_get = 7  # obj.over_no_get赋值会触发描述符的__set__方法
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get
    <p527_descriptor_kinds.OverridingNoGet object at 0x00000222BC4C8B38>
    >>> obj.__dict__['over_no_get'] = 9  # 通过实例的__dict__属性设置名为over_no_get的实例属性
    >>> obj.over_no_get  # over_no_get实例属性会遮盖描述符，但是只有读操作是如此
    9
    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # 只要实例有同名的实例属性，描述符就会被遮盖
    9
    """

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NoOverriding:
    """非覆盖型描述符
    没有实现__set__方法的描述符是非覆盖型描述符。如果设置了同名的实例属性，描述符会被遮盖，致使描述符无法处理
    那个实例的那个属性

    方法是以非覆盖型描述符实现的

    >>> obj = Managed()
    >>> obj.non_over
    -> NoOverriding.__get__(<NoOverriding object>, <Managed object>, <class Managed>)
    >>> obj.non_over = 7
    >>> obj.non_over  # obj有个名为non_over的实例属性，把Managed类的同名描述符属性遮盖掉
    7
    >>> Managed.non_over
    -> NoOverriding.__get__(<NoOverriding object>, None, <class Managed>)
    >>> del obj.non_over
    >>> obj.non_over
    -> NoOverriding.__get__(<NoOverriding object>, <Managed object>, <class Managed>)
    """

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    """在类中覆盖描述符
    不管描述符是不是覆盖型，为类属性赋值都能*覆盖*描述符

    示例揭示了读写属性的另一种不对等：读类属性的操作可以由依附在托管类上定义有__get__方法的描述符处理，
    但是写类属性的操作不会由依附在托管类上定义有__set__方法的描述符处理

    若想控制设置类属性的操作，要把描述符依附在类的类上，即依附在元类上。默认情况下，对用户定义的类来说，其元类是type，
    而我们不能为type添加属性。不过在第21章，我们会自己创建元类。
    """
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NoOverriding()

    def spam(self):
        print('-> Managed.spam({})'.format(display(self)))


if __name__ == '__main__':
    obj = Managed()
    print(Managed.over)
    Managed.over = 1  # 不对等，Managed.over调用了描述符的__get__，Managed.over = 1并没有调用描述符的__set__
    Managed.over_no_get = 2
    Managed.non_over = 3
    print(obj.over, obj.over_no_get, obj.non_over)
    # 1 2 3

