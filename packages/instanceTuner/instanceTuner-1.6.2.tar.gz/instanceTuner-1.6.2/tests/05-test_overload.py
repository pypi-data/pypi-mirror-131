from instanceTuner.operator import *
from instanceTuner.set import setFunction


def printException(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
        print('there is no error')
    except Exception as e:
        print(e)


@setFunction
def test():
    print('first test')


@setFunction
def test(x: str):
    print('second test', x)


@setFunction
def test(x: int):
    print('third test', x)


test()
test('2nd')
test(3)
printException(test, 4.0)

print('\n'*2)


Number = InstanceOperator('or', int, float)


class Test2:
    @setFunction
    def __init__(self, a: Number, b: Number) -> None:
        super().__init__()
        self.a = a
        self.b = b

    @setFunction
    def __init__(self, a: Number) -> None:
        super().__init__()
        self.a = a
        self.b = a

    def get(self):
        return self.a * self.b


print('Test2')

t = Test2(4)
print(t.get())

t = Test2(4, 5)
print(t.get())

printException(Test2)

print('\n'*2)


NotNumber = InstanceOperator('not', Number)


class Test3:
    @setFunction
    def __init__(self, a: Number, b: Number) -> None:
        super().__init__()
        self.a = a
        self.b = b

    @setFunction
    def __init__(self, a: NotNumber, b: NotNumber) -> None:
        super().__init__()
        self.a = a + a
        self.b = b + b

    def get(self):
        return self.a + self.b


print('Test3')

t = Test3(4, 5)
print(t.get())

t = Test3('4', '5')
print(t.get())

printException(Test3)

print('\n'*2)


print('MapInstances :\n')


class Test:

    def __init__(self) -> None:
        pass


miT = MapInstances(tuple, InstanceOperator('or', str, Test))


@setFunction
def tst() -> miT:
    return tuple([Test()])


@setFunction
def testTuple(*args: miT):
    print('testTuple')
    print(len(args))


miT2 = MapInstances(tuple, InstanceOperator('not', str, Test))


@setFunction
def tst2() -> miT2:
    return tuple([[]])


@setFunction
def testTuple(*args: miT2):
    print('testTuple 2')
    print(len(args))


miT3 = MapInstances(tuple, RepeatBoundary(2, 4), Test)


@setFunction
def tst4() -> miT3:
    return tuple([Test() for i in range(3)])


@setFunction
def testTuple(*args: miT3):
    print('testTuple 3')
    print(len(args))


@setFunction
def testTuple2(*args: miT3):
    print('testTuple2')
    print(len(args))


miD = MapInstances(dict, 'dict', RepeatBoundary(3), {'k': str, 'v': int})


@setFunction
def tst5() -> miD:
    return {str(i): i for i in range(4)}


@setFunction
def testDict(**kwargs: miD):
    print('testDict')
    print(len(kwargs))


miD3 = MapInstances(dict, 'dict',
                    RepeatBoundary(1, 3),
                    {'k': str, 'v': miT3})


@setFunction
def tst8() -> miD3:
    return {'a': tst4(), 'b': tst4()}


@setFunction
def testDict(**kwargs: miD3):
    print('testDict 3')
    print(len(kwargs))


print('testTuples :: \n\n')

testTuple(*tst())
testTuple(*[Test()])
testTuple(*['tt'])
testTuple(*tst2())
testTuple(*[2])
testTuple(*tst4())
testTuple(*[Test()]*2)
testTuple2(*[Test()]*2)


print('printExceptions :: \n\n')

printException(testTuple)
print('*\n'*3)
printException(testTuple2, *tuple([Test()]*3))
print('*\n'*3)
printException(testTuple2, *tuple([Test()]*6))


print('testDicts :: \n\n')

testDict(**tst5())
testDict(**{str(i): i for i in range(5, 9)})
testDict(**tst8())


print('printExceptions :: \n\n')

printException(testDict)
printException(testDict, **{'a': 4})
