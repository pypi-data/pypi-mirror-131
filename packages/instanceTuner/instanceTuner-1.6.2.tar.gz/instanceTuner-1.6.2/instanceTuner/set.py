from CAImport.tools import Singleton, hasInstancecheck as hic
from inspect import _ParameterKind, Parameter, signature, _empty
import sys
from typing import Any


def getNameOrSelf(obj):
    try:
        return obj.__name__
    except Exception:
        return obj


class Arg:
    """
    It keeps Parameter instance and sets value for it

    __init__ argument:
    arg: a Parameter instance

    usage: setValue method sets passed value if value
    is _empty and if the type of passed value is instance
    of self.arg.annotation; otherwise raises an error
    """

    def __init__(self, arg) -> None:
        """
        __init__ argument:
        arg: a Parameter instance
        """

        assert isinstance(arg, Parameter)
        self.arg = arg
        self.value = _empty

    def setValue(self, value):
        """
        setValue method sets passed value if value
        is _empty and if the type of passed value is instance
        of self.arg.annotation; otherwise raises an error
        """

        if self.value != _empty:
            raise ValueError('got multiple values.')

        if self.arg.annotation != Any and \
                self.arg.annotation != _empty:
            if not isinstance(value, self.arg.annotation):
                raise TypeError('not match with annotation')

        self.value = value

    def __repr__(self) -> str:
        return str({'name': self.arg.name,
                    'kind': self.arg.kind,
                    'annotation': self.arg.annotation,
                    'default': self.arg.default,
                    'value': self.value})


class ArgsCheck:
    """
    It keeps a function and check inputs and outputs

    __init__ argument:
    fn: a function

    3 uses:

    1 assert_ :
    we pass arguments of self.fn as *args and **kwargs
    and if it was'nt match with annotations, it raises an error

    2 return_ :
    we pass arguments of self.fn as *args and **kwargs
    and if its return value was'nt match with annotation, it raises
    an error

    3 @staticmethod find :
    we pass functions and arguments as selves *args and **kwargs
    selves must be tuple or list of ArgsCheck instances 
    this method raturns the first function which its assert_ method 
    does'nt raise an error and if there isn't a single function which
    its arguments matches, it raises an error
    """

    def __init__(self, fn) -> None:
        """
        __init__ argument:
        fn: a function
        """
        assert callable(fn), 'fn must be a callable'
        self.fn = fn

        self.POSITIONAL_ONLY = []
        self.POSITIONAL_OR_KEYWORD = []
        self.VAR_POSITIONAL = None
        self.KEYWORD_ONLY = []
        self.VAR_KEYWORD = None
        self.cache = []

        self.fQual = f' module: {fn.__module__}' + \
            f' function: {fn.__qualname__}'

        self.argTXT = ' arg: {argName}'

        self.sig = f' signature: {signature(self.fn)}'

        self.eTXT = self.fQual + self.argTXT + self.sig

        self.annotationError = 'Expected {annotation}' + \
                               ' but received {argType}.' + \
                               self.eTXT

        self.pOnlyMissingError = self.fQual + \
            ' takes at least {takes} positional args' + \
            ' but {given} has been given.' + \
            self.sig

        self.argMissingError = 'an argument has not been passed.' + \
                               self.eTXT

        self.argExtraError = self.fQual + \
            ' takes {takes} {kind} arguments' + \
            ' but at least {given} was given' + \
            self.sig

        self.returnError = 'returned value of' + \
            self.fQual + \
            ' was {ret}' + \
            ' but expected {annotation}' + \
            self.sig

        self.set()

    def __repr__(self) -> str:
        return str(self.__dict__)

    def set(self):

        for i in signature(self.fn).parameters.items():

            if i[1].kind in (
                _ParameterKind.POSITIONAL_ONLY,
                _ParameterKind.POSITIONAL_OR_KEYWORD,
                _ParameterKind.KEYWORD_ONLY
            ):
                getattr(self, i[1].kind.name).append(Arg(i[1]))

            else:
                setattr(self, i[1].kind.name, Arg(i[1]))

    def clearCache(self):
        for arg in self.cache:
            arg.value = _empty

    def setValue(self, arg, value):
        try:
            arg.setValue(value)
            self.cache.append(arg)
        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()

            if exc_type == TypeError:
                strE = self.annotationError
                raise TypeError(strE.format(annotation=getNameOrSelf(arg.arg.annotation),
                                            argType=type(value).__name__,
                                            argName=arg.arg.name))

            else:
                strE = str(e) + self.eTXT
                raise ValueError(strE.format(argName=arg.arg.name))

    def assert_(self, *args, **kwargs):
        """
        we pass arguments of self.fn as *args and **kwargs
        and if it was'nt match with annotations, it raises an error
        """

        def argsAssert(args_):
            for arg in args_:
                if arg.arg.default == _empty:
                    assert arg.value != _empty,\
                        self.argMissingError.format(argName=arg.arg.name)

        def setValues(args_, values):
            for i in range(len(values)):
                self.setValue(args_[i], values[i])

        def setPOnly(args_):
            assert len(args_) >= len(self.POSITIONAL_ONLY),\
                self.pOnlyMissingError.format(takes=len(self.POSITIONAL_ONLY),
                                              given=len(args_))

            pOnly = args_[:len(self.POSITIONAL_ONLY)]
            setValues(self.POSITIONAL_ONLY, pOnly)
            return args_[len(self.POSITIONAL_ONLY):]

        def setPK(args_):
            min_ = min(len(self.POSITIONAL_OR_KEYWORD), len(args_))
            pk = args_[:min_]
            setValues(self.POSITIONAL_OR_KEYWORD, pk)
            return args_[min_:]

        def setVP(args_):
            if self.VAR_POSITIONAL is None and \
                    len(args_) > 0:
                raise TypeError(self.argExtraError.format(
                    takes=len(self.POSITIONAL_ONLY),
                    given=len(self.POSITIONAL_ONLY) + len(args_),
                    kind='positional'))

            elif self.VAR_POSITIONAL is None:
                return

            self.setValue(self.VAR_POSITIONAL, args_)

        def setKWValues(args_, KWDict):
            theyreIn = []
            for arg in args_:
                if arg.arg.name in KWDict:
                    self.setValue(arg, KWDict[arg.arg.name])
                    theyreIn.append(arg.arg.name)

            return {k: v for k, v in KWDict.items() if k not in theyreIn}

        def setKOnly(kws):
            kws = setKWValues(self.KEYWORD_ONLY, kws)
            argsAssert(self.KEYWORD_ONLY)
            return kws

        def setVK(kws):
            if self.VAR_KEYWORD is None and \
                    len(kws) > 0:
                raise TypeError(self.argExtraError.format(
                    takes=len(self.KEYWORD_ONLY),
                    given=len(self.KEYWORD_ONLY) + len(kws),
                    kind='keyword'))

            elif self.VAR_KEYWORD is None:
                return

            self.setValue(self.VAR_KEYWORD, kwargs)

        self.clearCache()

        args = setPOnly(args)
        args = setPK(args)
        setVP(args)

        kwargs = setKOnly(kwargs)
        kwargs = setKWValues(self.POSITIONAL_OR_KEYWORD,
                             kwargs)   # setPK
        setVK(kwargs)

        argsAssert(self.POSITIONAL_OR_KEYWORD)

    def returnAssert(self, ret):

        if 'return' in self.fn.__annotations__:

            annotation = getNameOrSelf(self.fn.__annotations__["return"])

            if hic(self.fn.__annotations__['return']):

                assert self.fn.__annotations__['return'] == Any or \
                    isinstance(ret, self.fn.__annotations__['return']),\
                    self.returnError.format(ret=type(ret).__name__,
                                            annotation=annotation)
                return

            assert ret == self.fn.__annotations__['return'],\
                self.returnError.format(ret=ret,
                                        annotation=annotation)

    def return_(self, *args, **kwargs):
        """
        we pass arguments of self.fn as *args and **kwargs
        and if its return value was'nt match with annotation, it raises
        an error
        """

        ret = self.fn(*args, **kwargs)
        self.returnAssert(ret)
        return ret

    @staticmethod
    def find(selves, *args, **kwargs):
        """
        we pass functions and arguments as selves *args and **kwargs
        selves must be tuple or list of ArgsCheck instances 
        this method raturns the first function which its assert_ method 
        does'nt raise an error and if there isn't a single function which
        its arguments matches, it raises an error
        """

        errors = ["base of these entries, no matching function found."]
        for self in selves:
            try:
                self.assert_(*args, **kwargs)
                return self
            except Exception as e:
                errors.append(str(e))

        assert False, '\n\n'.join(errors)


# ********************
# I've copied and changed every code bellow from:
# https://www.codementor.io/@arpitbhayani/overload-functions-in-python-13e32ahzqt

class Function(ArgsCheck):
    """Function is a wrap over standard python function

    When the Call is called, like a function, it fetches
    the function to be invoked from the virtual namespace and then
    invokes the same.

    __init__ argument:
    fn: a function
    """

    def __init__(self, fn) -> None:
        """
        __init__ argument:
        fn: a function
        """

        super().__init__(fn)

    @staticmethod
    def Call(self):
        """
        When the Call is called, like a function, it fetches
        the function to be invoked from the virtual namespace and then
        invokes the same.
        """

        def get(*args, **kwargs):
            # fetching the function to be invoked
            # from the virtual namespace
            # through the arguments.
            fns = Namespace().get(self.fn)
            assert fns is not None, "base of entered name and module, no matching function found."
            fn = ArgsCheck.find(fns, *args, **kwargs)

            # invoking the wrapped function and returning the value.
            return fn.return_(*args, **kwargs)

        return get


class Namespace(Singleton):
    """Namespace is the singleton class that is responsible
    for holding all the functions by their module name,
    class and their actual name and find it base on those.
    it come in handy for overload purposes or checking annotations

    usage: set a function like this:
    NameSpace.getInstance.register(fn)

    it would wrap fn for overload purposes or checking annotations
    """

    def __init__(self):
        self.function_map = dict()

    @staticmethod
    def key(fn):
        return fn.__module__, fn.__qualname__

    def register(self, fn):
        """
        registers the function in the virtual namespace and returns
        Function.Call(Function(fn)) that wraps the
        function fn.
        """
        func = Function(fn)
        key = Namespace.key(fn)

        if key in self.function_map:
            self.function_map[key] = [func] + \
                self.function_map[key]
        else:
            self.function_map[key] = [func]

        return Function.Call(func)

    def get(self, fn):
        """
        get returns the matching function from the virtual namespace.
        return None if it did not fund any matching function.
        """
        return self.function_map.get(Namespace.key(fn))


def setFunction(fn):
    """
    setFunction is the decorator that wraps the function
    and returns a callable object for overload purposes or 
    checking annotations
    """
    return Namespace().register(fn)
