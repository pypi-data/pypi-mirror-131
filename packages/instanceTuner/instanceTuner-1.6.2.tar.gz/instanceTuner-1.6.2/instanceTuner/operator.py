from typing import Any
from CAImport.tools import isIter, hasInstancecheck as hic


class CustomizeOperator:

    """
    It's customizes operator to implement
    __instancecheck__

    __init__ arguments:
    fn: callable 
    *args: fn args
    **kwargs: fn kwargs

    fn must be able to receive and handle a keyword
    argument named __instance and must return boolean
    """

    def __init__(self, fn, *args, **kwargs) -> None:
        """
        __init__ arguments:
        fn: callable 
        *args: fn args
        **kwargs: fn kwargs
        """

        assert callable(fn), 'fn must be callable'
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return f'fn doc: {self.fn.__doc__}' + \
            f' args: {self.args} kwargs: {self.kwargs}'

    def __instancecheck__(self, __instance: Any) -> bool:
        """
        fn must be able to receive and handle a keyword
        argument named __instance and must return boolean
        """

        self.kwargs['__instance'] = __instance
        return self.fn(*self.args, **self.kwargs)


class ClassOperator:

    """
    We wanna say if an object is equal 
    to a class by using isinstance method.

    its __init__ takes one arguments :
    cls: must be a class

    for example :

    iop = InstanceOperator(
    'or', Test, ClassOperator(Test))

    print(isinstance(Test, iop))   # True
    print(isinstance(Test(), iop)) # True

    iop = InstanceOperator(
        'not', Test, ClassOperator(Test))

    print(isinstance(Test, iop))   # False
    print(isinstance(Test(), iop)) # False
    """

    def __init__(self, cls) -> None:
        """
        __init__ takes one arguments :
        cls: must be a class
        """

        assert getattr(cls, '__init__'), 'cls must be a class'
        self.cls = cls

    def __repr__(self) -> str:
        return f'{self.cls}'

    def __instancecheck__(self, __instance) -> bool:
        return __instance is self.cls

    @staticmethod
    def setClasses(classes):
        return [ClassOperator(cls) for cls in classes]


class Operator:

    """
    This class is just a base class for
    ClassOperator and InstanceOperator
    """

    def __init__(self, operator: str) -> None:
        """
        operator: an string which must be 'or' or 'not'
        """

        assert operator in ('or', 'not'), 'use "or" "not"'
        self.operator = operator


class InstanceOperator(Operator):

    """
    A class to do isinstance job, 
    an alternative which is reusable by its instance

    it tells you if some object is instance of set of instances
    or in other usage, if its not.

    its __init__ takes at least two arguments :
    operator: an string which must be 'or' or 'not'
    *instances: must use at least one Variable Positional for it and
    these Variables must be a class or instance which have __instancecheck__

    operator will use for determine if instances
    are what we want or what we avoid

    for using it you should use: 
    isinstance(someInstance, instanceOfInstanceOperator)

    it tells you if someInstance is instance of instanceOfInstanceOperator
    or not, by returning True if it's actually an instance and operator is 'or',
    or ruturns False if it's not actually an instance and operator is 'or',
    or ruturns True if it's not actually an instance and operator is 'not',
    or ruturns False if it's actually an instance and operator is 'not'.
    """

    def __init__(self, operator: str, *instances) -> None:
        """
        __init__ takes at least two arguments :
        operator: an string which must be 'or' or 'not'
        *instances: must use at least one Variable Positional for it and
        these Variables must be a class or instance which have __instancecheck__

        operator will use for determine if instances
        are what we want or what we avoid
        """

        super().__init__(operator)

        assert len(
            instances) > 0, 'this class operat on instances, you must use instances too'

        for i in instances:
            assert hic(i)

        self.instances = instances

    def __repr__(self) -> str:
        result = f' {self.operator} '.join([str(i) for i in self.instances])
        return result if self.operator == 'or' else ' not ' + result

    def __instancecheck__(self, __instance) -> bool:
        """
        this method returns True if __instance 
        is actually an instance of instances and operator is 'or',
        or ruturns False if it's not actually an instance and operator is 'or',
        or ruturns True if it's not actually an instance and operator is 'not',
        or ruturns False if it's actually an instance and operator is 'not'.
        """

        if self.operator == 'or':
            # 'or'
            for i in self.instances:
                if isinstance(__instance, i):
                    return True
            return False

        # 'not'
        for i in self.instances:
            if isinstance(__instance, i):
                return False
        return True


class ObjectOperator(InstanceOperator):

    """
    A class based on InstanceOperator for completing it

    if we use this class instead of InstanceOperator,
    when __instancecheck__ is called and self.operator
    is 'or', we are saying if an object is instance of
    a class or the class itself.
    when self.operator is 'not', we are saying if 
    an object is not instance of a class and 
    not the class itself.

    its __init__ takes at least two arguments :
    operator: an string which must be 'or' or 'not'
    *instances: must use at least one Variable Positional for it and
    these Variables must be a class or an instance of a class with 
    __instancecheck__

    operator will use for determine if instances
    are what we want or what we avoid

    for example:

    oop = ObjectOperator('or', Test)

    print(isinstance(Test, oop))   # True
    print(isinstance(Test(), oop)) # True

    oop = ObjectOperator('not', Test)

    print(isinstance(Test, oop))   # False
    print(isinstance(Test(), oop)) # False
    """

    def __init__(self, operator: str, *instances) -> None:
        """
        __init__ takes at least two arguments :
        operator: an string which must be 'or' or 'not'
        *instances: must use at least one Variable Positional for it and
        these Variables must be a class or an instance of a class with 
        __instancecheck__

        operator will use for determine if instances
        are what we want or what we avoid
        """

        objects = instances + tuple(ClassOperator.setClasses(instances))
        super().__init__(operator, *objects)


class RepeatBoundary:

    """
    A class to check minimum and maximum of a repetition

    After initialization you should use _instance.checkRepeat(count)
    and it returns boolean
    """

    def __init__(self, min_, max_=None) -> None:
        """
        __init__ takes at least one argument which is min_
        min_ and max_ must be integer 
        max_ must be equal or greater than min_
        """
        assert isinstance(min_, int) and min_ >= 0
        assert (isinstance(max_, int) and min_ <= max_) or max_ is None
        self.min = min_
        self.max = max_

    def checkRepeat(self, count):
        """
        A method to check minimum and maximum of a repetition
        """

        if self.max is not None:
            if count > self.max:
                return False

        return self.min <= count

    def __repr__(self) -> str:
        return f'(min: {self.min}, max: {self.max})'


class MapInstances:

    """
    This class use to check type of instances of an iterable items

    its __init__ takes at least one argument which is instance_

    __init__ arguments:
    instance_: it would be type of iterable which will compare later with the
    iterable that is gonna passed into __instancecheck__ method

    mapTuple: is tuple of types or instances with __instancecheck__
    which will compare later with the iterable items

    every mapTuple item can be RepeatBoundary instance which goes a type
    or instance with __instancecheck__ after it. note that it can't be
    followed by another RepeatBoundary. After another object which is not
    RepeatBoundary, the mapTuple can goes with another RepeatBoundary followed 
    by non RepeatBoundary object.

    whole RepeatBoundary thing is for counting repetition of an object in mapTuple

    usage :
    isinstance(someIter, mapInstancesObj) :
    returns True if someIter and its items are instances of mapInstancesObj
    and returns False if are'nt.
    """

    def __init__(self, instance_, *mapTuple) -> None:
        """
        __init__ arguments:
        instance_: it would be type of iterable which will compare later with the
        iterable that is gonna passed into __instancecheck__ method

        mapTuple: is tuple of types or instances with __instancecheck__
        which will compare later with the iterable items

        every mapTuple item can be RepeatBoundary instance which goes a type
        or instance with __instancecheck__ after it. note that it can't be
        followed by another RepeatBoundary. After another object which is not
        RepeatBoundary, the mapTuple can goes with another RepeatBoundary followed 
        by non RepeatBoundary object.

        whole RepeatBoundary thing is for counting repetition of an object in mapTuple

        for more explanation about using key value pair or index value pair iterables
        check out : 
        """
        self.instance = instance_
        self.setMapTuple(*mapTuple)

    def setMapTuple(self, *mapTuple):
        if len(mapTuple) == 0:
            self.mapTuple = mapTuple
            return

        def tupleCheck():
            index = 0
            while index < len(mapTuple):
                if isinstance(mapTuple[index], RepeatBoundary):
                    index += 1
                    assert index < len(
                        mapTuple), 'mapTuple format is wrong, must be an object after RepeatBoundary'
                    assert not isinstance(
                        mapTuple[index], RepeatBoundary), 'mapTuple format is wrong, must be an object after RepeatBoundary, not a RepeatBoundary again'

                index += 1

        def dictCheck():
            index = 1
            while index < len(mapTuple):
                if isinstance(mapTuple[index], RepeatBoundary):
                    index += 1
                    assert index < len(
                        mapTuple), 'mapTuple format is wrong, must be an object after RepeatBoundary'
                    assert not isinstance(
                        mapTuple[index], RepeatBoundary), 'mapTuple format is wrong, must be an object after RepeatBoundary, not a RepeatBoundary again'
                    continue

                if mapTuple[index] == Any:
                    index += 1
                    continue

                assert isinstance(
                    mapTuple[index], dict), 'in dict objects you should use dictionary for each key and value pair'

                assert 'k' in mapTuple[index] and 'v' in mapTuple[
                    index], 'your dictionary must determine key with "k": object and value with "v": object pairs'

                index += 1

            assert index > 1, 'nothing received! you must complete the dictionary'

        dictCheck() if mapTuple[0] == 'dict' else tupleCheck()
        self.mapTuple = mapTuple

    def __instancecheck__(self, __instance: Any) -> bool:
        """
        isinstance(__instance, mapInstancesObj) :
        returns True if __instance and its items are instances of mapInstancesObj
        and returns False if are'nt.
        """

        def patternAssert(I, pattern):

            def tupleAssert(i, p):
                def tuLastIndex(i_, iIndex_, p_):
                    try:
                        patternAssert(i_[iIndex_], p_)
                        return tuLastIndex(i_, iIndex_+1, p_)
                    except Exception as e:
                        return iIndex_

                def tuFirstMatch(i_, x, lastX, p_):
                    while x <= lastX + 1:
                        try:
                            tupleAssert(i_[x:], p_)
                            return True
                        except Exception as e:
                            x += 1
                    return False

                iIndex = -1
                pIndex = -1

                while pIndex < len(p) - 1:

                    iIndex += 1
                    pIndex += 1

                    assert iIndex < len(
                        i), 'instance and pattern are not match1'

                    if isinstance(p[pIndex], RepeatBoundary):
                        rb = p[pIndex]
                        pIndex += 1
                        lastIndex = tuLastIndex(i, iIndex, p[pIndex])

                        assert rb.checkRepeat(
                            lastIndex - iIndex), 'instance and pattern repetition are not match2'

                        iIndex2 = iIndex + rb.min

                        assert tuFirstMatch(i,
                                            iIndex2,
                                            lastIndex - 1,
                                            p[pIndex+1:]), \
                            'instance and pattern repetition are not match3'

                        return

                    else:
                        patternAssert(i[iIndex], p[pIndex])

                assert iIndex >= len(
                    i) - 1, 'instance and pattern are not match4'

            def dictAssert(i, p):
                def diLastIndex(i_, iIndex_, p_):
                    try:
                        patternAssert(i_[iIndex_]['k'], p_['k'])
                        patternAssert(i_[iIndex_]['v'], p_['v'])
                        return diLastIndex(i_, iIndex_+1, p_)
                    except Exception as e:
                        return iIndex_

                def diFirstMatch(i_, x, lastX, p_):
                    while x <= lastX + 1:
                        try:
                            dictAssert({j['k']: j['v'] for j in i_[x:]}, p_)
                            return True
                        except Exception as e:
                            x += 1
                    return False

                i = [{'k': k, 'v': i[k]} for k in i]
                iIndex = -1
                pIndex = -1

                while pIndex < len(p) - 1:

                    iIndex += 1
                    pIndex += 1

                    assert iIndex < len(
                        i), 'instance and pattern are not match5'

                    if isinstance(p[pIndex], RepeatBoundary):
                        rb = p[pIndex]
                        pIndex += 1
                        lastIndex = diLastIndex(i, iIndex, p[pIndex])

                        assert rb.checkRepeat(
                            lastIndex - iIndex), 'instance and pattern repetition are not match6'

                        iIndex2 = iIndex + rb.min

                        assert diFirstMatch(i,
                                            iIndex2,
                                            lastIndex - 1,
                                            p[pIndex+1:]), \
                            'instance and pattern repetition are not match7'

                        return

                    elif isinstance(p[pIndex], dict):
                        patternAssert(i[iIndex]['k'], p[pIndex]['k'])
                        patternAssert(i[iIndex]['v'], p[pIndex]['v'])

                    elif p[pIndex] == Any:
                        return

                    else:
                        raise Exception('your mapTuple design is wrong')

                assert iIndex >= len(
                    i) - 1, 'instance and pattern are not match8'

            if pattern == Any:
                return

            if isinstance(pattern, MapInstances):
                assert isinstance(
                    I, pattern), 'instance and pattern are not match9'
                return

            if isIter(pattern):
                dictAssert(I, pattern[1:]) if pattern[0] == 'dict' else tupleAssert(
                    I, pattern)
            else:
                assert isinstance(
                    I, pattern), 'instance and pattern are not match10'

        # **************************************
        # just a separator
        # **************************************

        if self.instance == Any:
            return True

        if not isinstance(__instance, self.instance):
            return False

        if len(self.mapTuple) > 0:
            try:
                patternAssert(__instance, self.mapTuple)
                return True
            except Exception as e:
                return False

        return isinstance(__instance, self.instance)

    def __repr__(self) -> str:

        def getMT():
            for mt in self.mapTuple:
                if isinstance(mt, dict):
                    yield tuple(('k:', k, 'v:', v)
                                for k, v in mt.items())
                else:
                    yield mt

        return f'(instance: {self.instance}, mapTuple: {tuple(mt for mt in getMT())})'
