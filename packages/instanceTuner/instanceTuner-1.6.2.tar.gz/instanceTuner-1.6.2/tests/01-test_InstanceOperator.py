from instanceTuner.operator import InstanceOperator


print(isinstance([], (str, list, tuple)))  # A or B: True
print(isinstance([], (dict, set)))  # A or B: False
print(not isinstance([], (dict, set)))  # not A and not B: True

# but we want object of equation to have sth reusable, so here it comes:

iOperator = InstanceOperator('not', str, list, tuple)
iOperator2 = InstanceOperator('or', dict, set)

iOperator3 = InstanceOperator('not', iOperator, iOperator2)
iOperator4 = InstanceOperator('or', iOperator, iOperator2)


print(isinstance([], iOperator))  # False
print(isinstance([], iOperator2))  # False
print(isinstance([], iOperator3))  # True
print(isinstance([], iOperator4))  # False

print(isinstance({}, iOperator))  # True
print(isinstance({}, iOperator2))  # True
print(isinstance({}, iOperator3))  # False
print(isinstance({}, iOperator4))  # True
