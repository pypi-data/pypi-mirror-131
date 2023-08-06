from instanceTuner.operator import *


class Test:

    def __init__(self) -> None:
        pass


mi = MapInstances(Test)
print(isinstance(Test(), mi), '# True', 'Test() -> Test')

mi = MapInstances(Any)
print(isinstance([Test()], mi), '# True', '[Test()] -> Any')

mi = MapInstances(list, Any)
print(isinstance([Test()], mi), '# True', '[Test()] -> list, Any')

mi = MapInstances(list, InstanceOperator('or', str, Test))
print(isinstance([Test()], mi), '# True',
      '[Test()] -> list, InstanceOperator("or", str, Test)')

mi = MapInstances(list, InstanceOperator('not', str, Test))
print(isinstance([Test()], mi), '# False',
      '[Test()] -> list, InstanceOperator("not", str, Test)')

mi = MapInstances(list, Test)
print(isinstance([Test()], mi), '# True', '[Test()] -> list, Test')

mi = MapInstances(list, RepeatBoundary(0), str, Test)
print(isinstance([Test()], mi), '# True',
      '[Test()] -> list, RepeatBoundary(0), str, Test')

mi = MapInstances(list, RepeatBoundary(1), str, Test)
print(isinstance(['abc', Test()], mi), '# True',
      '["abc", Test()] -> list, RepeatBoundary(1), str, Test')

mi = MapInstances(list, Test, Test)
print(isinstance([Test(), Test()], mi), '# True',
      '[Test(), Test()] -> list, Test, Test')


def tst():
    return [Test() for i in range(4)]


mi = MapInstances(dict)
print(isinstance(tst(), mi), '# False', 'tst() -> dict')

mi = MapInstances(list, Test)
print(isinstance(tst(), mi), '# False', 'tst() -> list, Test')

try:
    mi = MapInstances(list, RepeatBoundary(1, 4))
except Exception as e:
    print(e, '# will executed')
finally:
    print('list, RepeatBoundary(1, 4)', '# will executed')


mi = MapInstances(dict, RepeatBoundary(1, 4), Test)
print(isinstance(tst(), mi), '# False',
      'tst() -> dict, RepeatBoundary(1, 4), Test')

mi = MapInstances(list, RepeatBoundary(5, 6), Test)
print(isinstance(tst(), mi), '# False',
      'tst() -> list, RepeatBoundary(5, 6), Test')

mi = MapInstances(list, RepeatBoundary(1, 3), Test)
print(isinstance(tst(), mi), '# False',
      'tst() -> list, RepeatBoundary(1, 3), Test')

mi = MapInstances(list, RepeatBoundary(1, 4), Test)
print(isinstance(tst(), mi), '# True',
      'tst() -> list, RepeatBoundary(1, 4), Test')


def tst2():
    return {str(i): i for i in range(4)}


try:
    mi2 = MapInstances(dict, 'dict')
except Exception as e:
    print(e, '# will executed')
finally:
    print("dict, 'dict'", '# will executed')

mi2 = MapInstances(dict, 'dict', RepeatBoundary(4, 4), {'k': str, 'v': int})
print(isinstance(tst2(), mi2), '# True',
      "tst2() -> dict, 'dict', RepeatBoundary(4, 4), {'k': str, 'v': int}")

mi2 = MapInstances(dict, 'dict', RepeatBoundary(4, 4), {'k': int, 'v': int})
print(isinstance(tst2(), mi2), '# False',
      "tst2() -> dict, 'dict', RepeatBoundary(4, 4), {'k': int, 'v': int}")

mi2 = MapInstances(dict, 'dict',
                   RepeatBoundary(2, 4),
                   {'k': str, 'v': int},
                   RepeatBoundary(1, 3),
                   {'k': int, 'v': str})

print(isinstance({'a': 1, 'b': 2, 'c': 3, 1: 'a', 2: 'b'}, mi2), '# True',
      "{'a': 1, 'b': 2, 'c': 3, 1: 'a', 2: 'b'} -> dict, 'dict', RepeatBoundary(2, 4), {'k': str, 'v': int}, RepeatBoundary(1, 3), {'k': int, 'v': str}")


mi2 = MapInstances(dict, 'dict',
                   RepeatBoundary(1, 3),
                   {'k': str, 'v': mi})

print(isinstance({'a': tst(), 'b': tst()}, mi2), '# True',
      "{'a': tst(), 'b': tst()} -> dict, 'dict', RepeatBoundary(1, 3), {'k': str, 'v': mi}")
