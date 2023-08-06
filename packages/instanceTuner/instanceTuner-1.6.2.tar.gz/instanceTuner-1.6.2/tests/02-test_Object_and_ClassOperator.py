from instanceTuner.operator import *


class Test:

    pass


iop = InstanceOperator('or', int, Test)

print(isinstance(int, iop))
print(isinstance(1, iop))
print(isinstance(Test, iop))
print(isinstance(Test(), iop))

print('\n'*2)


iop = InstanceOperator('not', int, Test)

print(isinstance(int, iop))
print(isinstance(1, iop))
print(isinstance(Test, iop))
print(isinstance(Test(), iop))

print('\n'*2)


iop = InstanceOperator(
    'or', Test, ClassOperator(Test))

print(isinstance(Test, iop))
print(isinstance(Test(), iop))

print('\n'*2)


iop = InstanceOperator(
    'not', Test, ClassOperator(Test))

print(isinstance(Test, iop))
print(isinstance(Test(), iop))

print('\n'*2)


oop = ObjectOperator('or', Test)

print(isinstance(Test, oop))
print(isinstance(Test(), oop))

print('\n'*2)


oop = ObjectOperator('not', Test)

print(isinstance(Test, oop))
print(isinstance(Test(), oop))
