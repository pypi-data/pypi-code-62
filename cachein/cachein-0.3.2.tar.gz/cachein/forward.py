
from .member import Cached

class Forward(Cached):
    '''
    A caching delegate.  This brings a member or method into the containing
    instance lazily when accessed.
    
    >>> import cachein
    >>> class Greeter(object):
    ...     def __init__(self, recipient):
    ...         self.recipient = recipient
    ...
    ...     def greet(self):
    ...         return 'Hello, %s' % self.recipient
    
    >>> class Helper(object):
    ...     def __init__(self, greeter):
    ...         self.greeter = greeter
    ...
    ...     greet = recipient = Forward('greeter')

    >>> helper = Helper(Greeter('world'))
    >>> helper.greet()
    'Hello, world'
    >>> helper.recipient
    'world'
    
    >>> class RecipientHelper(object):
    ...     def __init__(self, recipient='world', greetercls=Greeter):
    ...         self.recipient = recipient
    ...         self.greetercls = greetercls
    ...
    ...     @cachein.Cached()
    ...     def greeter(self):
    ...         return self.greetercls(self.recipient)
    ...     greet = Forward(greeter)
    ...     who = Forward(greeter, 'recipient')

    >>> RecipientHelper().greet()
    'Hello, world'
    >>> RecipientHelper('everyone').greet()
    'Hello, everyone'
    >>> RecipientHelper('everyone').who
    'everyone'

    >>> @Forward.compose('greeter', 'greet', who='recipient')
    ... class ComposedHelper(object):
    ...     def __init__(self, greeter):
    ...         self.greeter = greeter
    
    >>> ComposedHelper(Greeter('world')).greet()
    'Hello, world'
    >>> ComposedHelper(Greeter('world')).who
    'world'
    
    >>> anyGreeter = Forward.composer('greet', who='recipient')
    >>> @anyGreeter.greeter('recipient', 'recipient', who=False)
    ... class AnyGreeterHelper(object):
    ...     def __init__(self, greeter):
    ...         self.greeter = greeter
    >>> AnyGreeterHelper(Greeter('world')).greet()
    'Hello, world'
    >>> AnyGreeterHelper(Greeter('world')).recipient
    'world'
    '''
    
    def __init__(self, source, attr=None, **_kw):
        super().__init__(source=source, attr=attr, **_kw)
        
    def init(self, source, attr, **_kw):
        super().init(**_kw)
        self.source = source
        self.attr = attr

    def getter(self):
        source = getattr(self.source, '__cachein_delegate_attr__', self.source)
            
        def delegate_getter(self, target, cls=None, name=self.name,
                            source=source, attr=self.attr or self.name):
            if target is None:
                return self     # (NO-COV-DT)
            else:
                obj = getattr(getattr(target, source), attr)
                target.__dict__[name] = obj
                return obj
        return delegate_getter

    @classmethod
    def compose(_cls, _source, *_args, **_kw):
        def decorator(cls):
            for arg in _args:
                if _kw.get(arg, True):
                    setattr(cls, arg, _cls(_source, arg, name=arg))
            for dest, attr in _kw.items():
                if attr:
                    setattr(cls, dest, _cls(_source, attr, name=dest))
            return cls                
        return decorator

    @classmethod
    def composer(_cls, *_args, **_kw):
        return _cls.Composer(_cls, _args, _kw)

    class Composer(object):
        def __init__(self, cls, args, kw):
            self.__cls = cls
            self.__args = args
            self.__kw = kw
            
        def __getattr__(self, name):
            return lambda *_a, **_kw: self.compose(name, *_a, **_kw)
            
        def compose(_self, _source, *_args, **_kw):
            args = _self.__args + _args
            kw = dict(_self.__kw, **_kw)
            return _self.__cls.compose(_source, *args, **kw)
