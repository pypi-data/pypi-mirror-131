# InstanceTuner
Set limited type instances and overload functions like Java in python

you can install it by:

    pip install instanceTuner    

Do you want to be able overload every function and method, even constructors (__init__) like Java in python?

Do you want to never write 'raise' or 'assert' in your python code when it comes to function arguments?

    from instanceTuner.set import setFunction
    
    class Test:
        @setFunction
        def __init__(self, a: int, b) -> None:
            pass
        
        @setFunction
        def __init__(self, a: int, b: str) -> None:
            pass



This package will raise error for you if 'a' does'nt get integer value 

with checking types by using 'setFunction' we are able to distinguish signatures of functions from each other like java compiler and using it for overload purposes

if you pass some object for 'b' which is'nt str, first __init__ would executed 

even the return value can raise an error. but it does'nt have any use for overload due.for example :

    @setFunction
    def test() -> None:
        return 0

