from typing import Any
from instanceTuner.operator import *
from instanceTuner.set import setFunction


def printException(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
        print('there is no error')
    except Exception as e:
        print(e)


# check input:


@setFunction
def test(p, p2: int, /,
         pk: Any, pk2: int, pk3=None, pk4: str = 's',
         *args: tuple,
         k, k2: int, k3=None, k4: str = 't',
         **kwargs: dict):

    print(p)
    print(p2)
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(args)
    print(k)
    print(k2)
    print(k3)
    print(k4)
    print(kwargs)


"""
printException(test)
printException(test, 'p')
printException(test, 'p', 'p2')
printException(test, 'p', 2)
printException(test, 'p', 2, 'pk')
printException(test, 'p', 2, 'pk', 'pk2')
printException(test, 'p', 2, 'pk', 12)
printException(test, 'p', 2, 'pk', 12, k='k')
printException(test, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test2(p, p2: int, /, pk: Any, pk2: int, pk3=None, pk4: str = 2, *, k, k2: int, k3=None, k4: str = 2, **kwargs):
    print(p)
    print(p2)
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(k)
    print(k2)
    print(k3)
    print(k4)
    print(kwargs)


"""
printException(test2)
printException(test2, 'p')
printException(test2, 'p', 'p2')
printException(test2, 'p', 2)
printException(test2, 'p', 2, 'pk')
printException(test2, 'p', 2, 'pk', 'pk2')
printException(test2, 'p', 2, 'pk', 12)
printException(test2, 'p', 2, 'pk', 12, k='k')
printException(test2, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test2, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test2, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test2, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test2, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test2, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test2, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test2, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test2, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test2, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test2, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test2, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test3(p, p2: int, /, pk: Any, pk2: int, pk3=None, pk4: str = 2, *args, k, k2: int, k3=None, k4: str = 2):
    print(p)
    print(p2)
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(k)
    print(k2)
    print(k3)
    print(k4)


"""
printException(test3)
printException(test3, 'p')
printException(test3, 'p', 'p2')
printException(test3, 'p', 2)
printException(test3, 'p', 2, 'pk')
printException(test3, 'p', 2, 'pk', 'pk2')
printException(test3, 'p', 2, 'pk', 12)
printException(test3, 'p', 2, 'pk', 12, k='k')
printException(test3, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test3, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test3, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test3, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4')
printException(test3, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4', pk3='pk3')
printException(test3, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test3, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test3, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test3, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test3, 'p', 2, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test3, 'p', 2, k2=22,
               k='k', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test3, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', k3=[], k4='k4')"""


@setFunction
def test4(p, p2: int, /, pk: Any, pk2: int, pk3=None, pk4: str = 's', *args, **kwargs):
    print(p)
    print(p2)
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(args)
    print(kwargs)


"""
printException(test4)
printException(test4, 'p')
printException(test4, 'p', 'p2')
printException(test4, 'p', 2)
printException(test4, 'p', 2, 'pk')
printException(test4, 'p', 2, 'pk', 'pk2')
printException(test4, 'p', 2, 'pk', 12)
printException(test4, 'p', 2, 'pk', 12, k='k')
printException(test4, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test4, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test4, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test4, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test4, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test4, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test4, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test4, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test4, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test4, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test4, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test4, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test5(p, p2: int, /, *args, k, k2: int, k3=None, k4: str = 't', **kwargs):
    print(p)
    print(p2)
    print(args)
    print(k)
    print(k2)
    print(k3)
    print(k4)
    print(kwargs)


"""
printException(test5)
printException(test5, 'p')
printException(test5, 'p', 'p2')
printException(test5, 'p', 2)
printException(test5, 'p', 2, 'pk')
printException(test5, 'p', 2, 'pk', 'pk2')
printException(test5, 'p', 2, 'pk', 12)
printException(test5, 'p', 2, 'pk', 12, k='k')
printException(test5, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test5, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test5, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test5, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test5, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test5, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test5, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test5, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test5, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test5, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test5, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test5, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test6(pk: Any, pk2: int, pk3=None, pk4: str = 's', *args, k, k2: int, k3=None, k4: str = 't', **kwargs):
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(args)
    print(k)
    print(k2)
    print(k3)
    print(k4)
    print(kwargs)


"""
printException(test6)
printException(test6, 'pk')
printException(test6, 'pk', 'pk2')
printException(test6, 'pk', 12)
printException(test6, 'pk', 12, k='k')
printException(test6, 'pk', 12, k2='k2', k='k')
printException(test6, 'pk', 12, k2=22, k='k')
printException(test6, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test6, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test6, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test6, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test6, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test6, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test6, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test6, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test6, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test6, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test7(p, p2: int, /, pk: Any, pk2: int, pk3=None, pk4: str = 2, *, k, k2: int, k3=None, k4: str = 2):
    print(p)
    print(p2)
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(k)
    print(k2)
    print(k3)
    print(k4)


"""
printException(test7)
printException(test7, 'p')
printException(test7, 'p', 'p2')
printException(test7, 'p', 2)
printException(test7, 'p', 2, 'pk')
printException(test7, 'p', 2, 'pk', 'pk2')
printException(test7, 'p', 2, 'pk', 12)
printException(test7, 'p', 2, 'pk', 12, k='k')
printException(test7, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test7, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test7, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test7, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4')
printException(test7, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test7, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test7, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test7, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test7, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test7, 'p', 2, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test7, 'p', 2, k2=22,
               k='k', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test7, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', k3=[], k4='k4')"""


@setFunction
def test8(p, p2: int, /, pk: Any, pk2: int, pk3=None, pk4: str = 's', *args):
    print(p)
    print(p2)
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(args)


"""
printException(test8)
printException(test8, 'p')
printException(test8, 'p', 'p2')
printException(test8, 'p', 2)
printException(test8, 'p', 2, 'pk')
printException(test8, 'p', 2, 'pk', 'pk2')
printException(test8, 'p', 2, 'pk', 12)
printException(test8, 'p', 2, 'pk', 12, k='k')
printException(test8, 'p', 2, 'pk', 12, pk3='pk3')
printException(test8, 'p', 2, 'pk', 12, pk3='pk3', pk4=14)
printException(test8, 'p', 2, 'pk', 12, pk3='pk3', pk4='pk4')
printException(test8, 'p', 2, 'pk', 12, pk3='pk3', pk4='pk4', pk='pk_')
printException(test8, 'p', 2, 'pk', 12, pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test8, 'p', 2, pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test8, 'p', 2, pk='pk_', pk2=12)
printException(test8, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16)"""


@setFunction
def test9(p, p2: int, /, *args, k, k2: int, k3=None, k4: str = 't'):
    print(p)
    print(p2)
    print(args)
    print(k)
    print(k2)
    print(k3)
    print(k4)


"""
printException(test9)
printException(test9, 'p')
printException(test9, 'p', 'p2')
printException(test9, 'p', 2)
printException(test9, 'p', 2, 'pk')
printException(test9, 'p', 2, 'pk', 'pk2')
printException(test9, 'p', 2, 'pk', 12)
printException(test9, 'p', 2, 'pk', 12, k='k')
printException(test9, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test9, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test9, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test9, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4')
printException(test9, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4', pk3='pk3')
printException(test9, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4')
printException(test9, 'p', 2, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')"""


@setFunction
def test10(pk: Any, pk2: int, pk3=None, pk4: str = 's', *args, k, k2: int, k3=None, k4: str = 't'):
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(args)
    print(k)
    print(k2)
    print(k3)
    print(k4)


"""
printException(test10)
printException(test10, 'pk')
printException(test10, 'pk', 'pk2')
printException(test10, 'pk', 12)
printException(test10, 'pk', 12, k='k')
printException(test10, 'pk', 12, k2='k2', k='k')
printException(test10, 'pk', 12, k2=22, k='k')
printException(test10, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test10, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4')
printException(test10, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4', pk3='pk3')
printException(test10, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test10, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test10, 'pk', 12, k2=22,
               k='k',  k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test10, 'pk', 12, k2=22,
               k='k',  k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test10, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test10, k2=22,
               k='k', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test10, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', k3=[], k4='k4')"""


@setFunction
def test11(p, p2: int, /, pk: Any, pk2: int, pk3=None, pk4: str = 's', **kwargs):
    print(p)
    print(p2)
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(kwargs)


"""
printException(test11)
printException(test11, 'p')
printException(test11, 'p', 'p2')
printException(test11, 'p', 2)
printException(test11, 'p', 2, 'pk')
printException(test11, 'p', 2, 'pk', 'pk2')
printException(test11, 'p', 2, 'pk', 12)
printException(test11, 'p', 2, 'pk', 12, k='k')
printException(test11, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test11, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test11, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test11, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test11, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test11, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test11, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test11, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test11, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test11, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test11, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test11, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test12(p, p2: int, /, *args, **kwargs):
    print(p)
    print(p2)
    print(args)
    print(kwargs)


"""
printException(test12)
printException(test12, 'p')
printException(test12, 'p', 'p2')
printException(test12, 'p', 2)
printException(test12, 'p', 2, 'pk')
printException(test12, 'p', 2, 'pk', 'pk2')
printException(test12, 'p', 2, 'pk', 12)
printException(test12, 'p', 2, 'pk', 12, k='k')
printException(test12, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test12, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test12, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test12, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test12, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test12, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test12, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test12, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test12, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test12, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test12, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test12, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test13(pk: Any, pk2: int, pk3=None, pk4: str = 's', *args, **kwargs):
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(args)
    print(kwargs)


"""
printException(test13)
printException(test13, 'pk')
printException(test13, 'pk', 'pk2')
printException(test13, 'pk', 12)
printException(test13, 'pk', 12, k='k')
printException(test13, 'pk', 12, k2='k2', k='k')
printException(test13, 'pk', 12, k2=22, k='k')
printException(test13, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test13, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test13, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test13, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test13, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test13, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test13, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test13, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test13, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test13, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test14(p, p2: int, /, *, k, k2: int, k3=None, k4: str = 't', **kwargs):
    print(p)
    print(p2)
    print(k)
    print(k2)
    print(k3)
    print(k4)
    print(kwargs)


"""
printException(test14)
printException(test14, 'p')
printException(test14, 'p', 'p2')
printException(test14, 'p', 2)
printException(test14, 'p', 2, 'pk')
printException(test14, 'p', 2, k='k')
printException(test14, 'p', 2, k2='k2', k='k')
printException(test14, 'p', 2, k2=22, k='k')
printException(test14, 'p', 2, k2=22, k='k', t=4, p='p')
printException(test14, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test14, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test14, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test14, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test14, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test14, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test14, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test14, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test14, 'p', 2, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test15(pk: Any, pk2: int, pk3=None, pk4: str = 's', *, k, k2: int, k3=None, k4: str = 't', **kwargs):
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(k)
    print(k2)
    print(k3)
    print(k4)
    print(kwargs)


"""
printException(test15)
printException(test15, 'pk')
printException(test15, 'pk', 'pk2')
printException(test15, 'pk', 12)
printException(test15, 'pk', 12, k='k')
printException(test15, 'pk', 12, k2='k2', k='k')
printException(test15, 'pk', 12, k2=22, k='k')
printException(test15, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test15, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test15, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test15, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test15, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test15, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test15, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test15, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test15, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test15, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test16(*args, k, k2: int, k3=None, k4: str = 't', **kwargs):
    print(args)
    print(k)
    print(k2)
    print(k3)
    print(k4)
    print(kwargs)


"""
printException(test16)
printException(test16, 'p')
printException(test16, 'p', 'p2')
printException(test16, 'p', 2)
printException(test16, 'p', 2, 'pk')
printException(test16, 'p', 2, 'pk', 'pk2')
printException(test16, 'p', 2, 'pk', 12)
printException(test16, 'p', 2, 'pk', 12, k='k')
printException(test16, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test16, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test16, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test16, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test16, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test16, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test16, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test16, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test16, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test16, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test16, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test16, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test17(p, p2: int, /, pk: Any, pk2: int, pk3=None, pk4: str = 's'):
    print(p)
    print(p2)
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)


"""
printException(test17)
printException(test17, 'p')
printException(test17, 'p', 'p2')
printException(test17, 'p', 2)
printException(test17, 'p', 2, 'pk')
printException(test17, 'p', 2, 'pk', 'pk2')
printException(test17, 'p', 2, 'pk', 12)
printException(test17, 'p', 2, 'pk', 12, k='k')
printException(test17, 'p', 2, 'pk', 12)
printException(test17, 'p', 2, 'pk', 12)
printException(test17, 'p', 2, 'pk', 12, pk3='pk3')
printException(test17, 'p', 2, 'pk', 12, pk3='pk3', pk4=14)
printException(test17, 'p', 2, 'pk', 12, pk3='pk3', pk4='pk4')
printException(test17, 'p', 2, 'pk', 12, pk3='pk3', pk4='pk4', pk='pk_')
printException(test17, 'p', 2, 'pk', 12, pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test17, 'p', 2, pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test17, 'p', 2, pk='pk_', pk2=12)
printException(test17, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test18(p, p2: int, /, *args):
    print(p)
    print(p2)
    print(args)


"""
printException(test18)
printException(test18, 'p')
printException(test18, 'p', 'p2')
printException(test18, 'p', 2)
printException(test18, 'p', 2, 'pk')
printException(test18, 'p', 2, 'pk', 'pk2')
printException(test18, 'p', 2, 'pk', 12)
printException(test18, 'p', 2, 'pk', 12, k='k')"""


@setFunction
def test19(pk: Any, pk2: int, pk3=None, pk4: str = 's', *args):
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(args)


"""
printException(test19)
printException(test19, 'pk')
printException(test19, 'pk', 'pk2')
printException(test19, 'pk', 12)
printException(test19, 'pk', 12, k='k')
printException(test19, 'pk', 12, pk3='pk3')
printException(test19, 'pk', 12, pk3='pk3', pk4=14)
printException(test19, 'pk', 12, pk3='pk3', pk4='pk4')
printException(test19, 'pk', 12, pk3='pk3', pk4='pk4', pk='pk_')
printException(test19, 'pk', 12,  pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test19, pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test19, pk='pk_', pk2=12)
printException(test19, 'pk', 12, 13, 'pk4', 15, 16)"""


@setFunction
def test20(p, p2: int, /, *, k, k2: int, k3=None, k4: str = 't'):
    print(p)
    print(p2)
    print(k2)
    print(k3)
    print(k4)


"""
printException(test20)
printException(test20, 'p')
printException(test20, 'p', 'p2')
printException(test20, 'p', 2)
printException(test20, 'p', 2, 'pk')
printException(test20, 'p', 2)
printException(test20, 'p', 2)
printException(test20, 'p', 2, k='k')
printException(test20, 'p', 2, k2='k2', k='k')
printException(test20, 'p', 2, k2=22, k='k')
printException(test20, 'p', 2, k2=22, k='k', t=4, p='p')
printException(test20, 'p', 2, k2=22,
               k='k', k3=[], k4='k4')"""


@setFunction
def test21(pk: Any, pk2: int, pk3=None, pk4: str = 's', *, k, k2: int, k3=None, k4: str = 't'):
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(k)
    print(k2)
    print(k3)
    print(k4)


"""
printException(test21)
printException(test21, 'pk')
printException(test21, 'pk', 'pk2')
printException(test21, 'pk', 12)
printException(test21, 'pk', 12, k='k')
printException(test21, 'pk', 12, k2='k2', k='k')
printException(test21, 'pk', 12, k2=22, k='k')
printException(test21, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test21, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4')
printException(test21, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4', pk3='pk3')
printException(test21, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test21, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test21, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test21, 'pk', 12, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test21, k2=22,
               k='k', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test21, k2=22,
               k='k', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test21, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', k3=[], k4='k4')"""


@setFunction
def test22(*args, k, k2: int, k3=None, k4: str = 't'):
    print(args)
    print(k)
    print(k2)
    print(k3)
    print(k4)


"""
printException(test22)
printException(test22, 'p')
printException(test22, 'p', 'p2')
printException(test22, 'p', 2)
printException(test22, 'p', 2, 'pk')
printException(test22, 'p', 2, 'pk', 'pk2')
printException(test22, 'p', 2, 'pk', 12)
printException(test22, 'p', 2, 'pk', 12, k='k')
printException(test22, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test22, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test22, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test22, 'p', 2, k2=22,
               k='k', k3=[], k4='k4')"""


@setFunction
def test23(p, p2: int, /, **kwargs):
    print(p)
    print(p2)
    print(kwargs)


"""
printException(test23)
printException(test23, 'p')
printException(test23, 'p', 'p2')
printException(test23, 'p', 2)
printException(test23, 'p', 2, 'pk')
printException(test23, 'p', 2, k='k')
printException(test23, 'p', 2, k2='k2', k='k')
printException(test23, 'p', 2, k2=22, k='k')
printException(test23, 'p', 2, k2=22, k='k', t=4, p='p')
printException(test23, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test23, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test23, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test23, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test23, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test23, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test23, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test23, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)"""


@setFunction
def test24(pk: Any, pk2: int, pk3=None, pk4: str = 's', **kwargs):
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)
    print(kwargs)


"""
printException(test24)
printException(test24, 'pk')
printException(test24, 'pk', 'pk2')
printException(test24, 'pk', 12)
printException(test24, 'pk', 12, k='k')
printException(test24, 'pk', 12, k2='k2', k='k')
printException(test24, 'pk', 12, k2=22, k='k')
printException(test24, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test24, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test24, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test24, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test24, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test24, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test24, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test24, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test24, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test24, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test25(*, k, k2: int, k3=None, k4: str = 't', **kwargs):
    print(k)
    print(k2)
    print(k3)
    print(k4)
    print(kwargs)


"""
printException(test25)
printException(test25, 'p')
printException(test25, k='k')
printException(test25, k2='k2', k='k')
printException(test25, k2=22, k='k')
printException(test25, k2=22, k='k', t=4, p='p')
printException(test25, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test25, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test25, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test25, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test25, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test25, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test25, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test25, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)"""


@setFunction
def test26(*args, **kwargs):
    print(args)
    print(kwargs)


"""
printException(test26)
printException(test26, 'p')
printException(test26, 'p', 'p2')
printException(test26, 'p', 2)
printException(test26, 'p', 2, 'pk')
printException(test26, 'p', 2, 'pk', 'pk2')
printException(test26, 'p', 2, 'pk', 12)
printException(test26, 'p', 2, 'pk', 12, k='k')
printException(test26, 'p', 2, 'pk', 12, k2='k2', k='k')
printException(test26, 'p', 2, 'pk', 12, k2=22, k='k')
printException(test26, 'p', 2, 'pk', 12, k2=22, k='k', t=4, p='p')
printException(test26, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4')
printException(test26, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4', pk3='pk3')
printException(test26, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4=14)
printException(test26, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4')
printException(test26, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_')
printException(test26, 'p', 2, 'pk', 12, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk2='pk2_')
printException(test26, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test26, 'p', 2, k2=22,
               k='k', t=4, p='p', k3=[], k4='k4',
               pk='pk_', pk2=12)
printException(test26, 'p', 2, 'pk', 12, 13, 'pk4', 15, 16,
               k2=22, k='k', t=4, p='p', k3=[], k4='k4')"""


@setFunction
def test27(p, p2: int, /):
    print(p)
    print(p2)


"""
printException(test27)
printException(test27, 'p')
printException(test27, 'p', 'p2')
printException(test27, 'p', 2)
printException(test27, 'p', 2, 'pk')
printException(test27, 'p', 2, k='k')"""


@setFunction
def test28(pk: Any, pk2: int, pk3=None, pk4: str = 's'):
    print(pk)
    print(pk2)
    print(pk3)
    print(pk4)


"""
printException(test28)
printException(test28, 'pk')
printException(test28, 'pk', 'pk2')
printException(test28, 'pk', 12)
printException(test28, 'pk', 12, 'pk3', 'pk4')
printException(test28, pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test28, 'pk', 12, 'pk3', 'pk4',
               pk3='pk3', pk4='pk4', pk='pk_', pk2=12)
printException(test28, 'pk', 12, k='k')
printException(test28, 'pk', 12, 13, 'pk4', 15, 16)"""


@setFunction
def test29(*args):
    print(args)


"""
printException(test29)
printException(test29, 'p')
printException(test29, 'p', 'p2')
printException(test29, 'p', 2)
printException(test29, 'p', 2, 'pk')
printException(test29, 'p', 2, 'pk', 'pk2')
printException(test29, 'p', 2, 'pk', 12)
printException(test29, 'p', 2, 'pk', 12, k='k')"""


@setFunction
def test30(*, k, k2: int, k3=None, k4: str = 't'):
    print(k)
    print(k2)
    print(k3)
    print(k4)


"""
printException(test30)
printException(test30, 'p')
printException(test30, k='k')
printException(test30, k2='k2', k='k')
printException(test30, k2=22, k='k', t=4, p='p')
printException(test30, k2=22, k='k', k3=[], k4='k4')"""


@setFunction
def test31(**kwargs):
    print(kwargs)


"""
printException(test31)
printException(test31, 'p')
printException(test31, k='k')
printException(test31, k2='k2', k='k')"""


@setFunction
def test32():
    print('test32')


"""
printException(test32)
printException(test32, 'p')
printException(test32, k='k')"""


# check returns:


class AcTest:

    @setFunction
    def __init__(self, x, y: int) -> None:
        self.x = x
        self.y = y
        print(x, y)

    @setFunction
    def getX(self) -> int:
        return self.x

    @setFunction
    def getY(self) -> int:
        return self.y


"""
printException(AcTest, 'x', 2)
printException(AcTest, 'x', 2.2)
printException(AcTest('x', 2).getY)
printException(AcTest('x', 2).getX)"""


class Test:

    def __init__(self) -> None:
        pass


mi = MapInstances(list, InstanceOperator('or', str, Test))


@setFunction
def tst() -> mi:
    return [Test()]


printException(tst)
print('tst no error \n')


mi = MapInstances(list, InstanceOperator('not', str, Test))


@setFunction
def tst2() -> mi:
    return [Test()]


printException(tst2)
print('tst2 error \n')


mi = MapInstances(list, RepeatBoundary(1, 3), Test)


@setFunction
def tst3() -> mi:
    return [Test() for i in range(4)]


printException(tst3)
print('tst3 error \n')


mi = MapInstances(list, RepeatBoundary(1, 4), Test)


@setFunction
def tst4() -> mi:
    return [Test() for i in range(4)]


printException(tst4)
print('tst4 no error \n')


mi2 = MapInstances(dict, 'dict', RepeatBoundary(4, 4), {'k': str, 'v': int})


@setFunction
def tst5() -> mi2:
    return {str(i): i for i in range(4)}


printException(tst5)
print('tst5 no error \n')


mi2 = MapInstances(dict, 'dict', RepeatBoundary(4, 4), {'k': int, 'v': int})


@setFunction
def tst6() -> mi2:
    return {str(i): i for i in range(4)}


printException(tst6)
print('tst6 error \n')

mi2 = MapInstances(dict, 'dict',
                   RepeatBoundary(2, 4),
                   {'k': str, 'v': int},
                   RepeatBoundary(1, 3),
                   {'k': int, 'v': str})


@setFunction
def tst7() -> mi2:
    return {'a': 1, 'b': 2, 'c': 3, 1: 'a', 2: 'b'}


printException(tst7)
print('tst7 no error \n')


mi2 = MapInstances(dict, 'dict',
                   RepeatBoundary(1, 3),
                   {'k': str, 'v': mi})


@setFunction
def tst8() -> mi2:
    return {'a': tst(), 'b': tst()}


printException(tst8)
print('tst8 no error \n')
