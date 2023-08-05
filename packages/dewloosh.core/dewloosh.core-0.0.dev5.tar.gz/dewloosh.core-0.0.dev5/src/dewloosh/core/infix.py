# -*- coding: utf-8 -*-
from collections.abc import Callable


class Infix:
    """
    Implements a custom Infix operator.

    Usage
    -----
        x |op| y    or    x <<op>> y

    Example
    -------
        >>> x = Infix(lambda x, y: x * y)
        >>> print(2 | x | 4)
        8

        >>> x = Infix(lambda x, y: x + y)
        >>> print(2 << x >> 4)
        6
    """

    def __init__(self, function: Callable):
        self.function = function

    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __or__(self, other):
        return self.function(other)

    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __rshift__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self.function(value1, value2)


if __name__ == '__main__':

    x = Infix(lambda x, y: x * y)
    print(2 | x | 4)

    x = Infix(lambda x, y: x + y)
    print(2 << x >> 4)

    # join = Infix(lambda x,y: x+y)
    # print(2 |join| 4)

    # def curry(f,x):
    #     def curried_function(*args, **kw):
    #         return f(*((x,)+args),**kw)
    #     return curried_function
    # curry = Infix(curry)
