class Cached(object):
    '''
    A caching member that derives its value from a decorated function.
    
    For example, a simple Vector class that can compute magnitude:
    
    >>> import cachein
    >>> class Vector(tuple):
    ...     @cachein.Cached()        # () is required!
    ...     def magnitude(self):
    ...         print("CALCULATING")
    ...         return sum(n ** 2 for n in self) ** .5
    
    >>> v = Vector((3, 4))
    >>> v.magnitude
    CALCULATING
    5.0
    
    If re-accesed, magnitude will not be calculated again.
    >>> v.magnitude
    5.0
   
    Note that there is no (easy) way to override mangnitude, so Cached() is 
    useful only if the class's version is completely definitive and should not 
    be overridden by a subclass.
    
    Use CachedAs() if overriding is needed.
    
    '''
    
    def __init__(self, **_kw):
        self.args = _kw
        self.init(**_kw)
        
    def init(self, name=None, fn=None):
        self.name = name
        self.fn = fn
        
    def __set_name__(self, target, name):
        setattr(target, name, self.clone(name=name))
            
    def clone(self, *, clonefactory=None, **_kw):
        factory = type(self) if clonefactory is None else clonefactory
        if not issubclass(factory, Cached): # (COV-NO-DT)
            raise TypeError('clone factory not from Cached: %r' % factory)
        return type(self)(**self.cloneargs(**_kw))
        
    def cloneargs(self, **_kw):
        return dict(self.args, **_kw)
    
    def __get__(self, target, cls=None):
        if target is None:
            return self         # (NO-COV)
        else:            
            getter = self.getter()
            cacher = type(
                self.name, 
                (object,), 
                { 
                    '__get__': getter, 
                    '__doc__': getter.__doc__,
                }
            )()
            self.__get__ = cacher.__get__
            return cacher.__get__(target, cls)

    def __call__(self, fn):
        return self.adopt(fn)

    def adopt(self, fn, **_kw):
        name = self.name
        if name is None:
            name = fn.__name__
        return self.clone(fn=fn, name=name, **_kw)

    def getter(self):
        def fn_getter(prop, target, cls=None, name=self.name, fn=self.fn):
            if target is None:
                return self         # (NO-COV)
            else:
                obj = fn(target)
                target.__dict__[name] = obj
                return obj
        return fn_getter
        
    @property
    def __cachein_delegate_attr__(self):
        return self.name
        
class CachedAs(Cached):
    '''
    A cached member that calls a CachedAs for its value.  This allows for
    inheritance to work to acquire the value, but caches the result in the
    specified attriubte name.
    
    Unlike the base Cached(), CachedAs() has two parts: the member to 
    save the value to and the member that will be called by name.
    
    >>> import cachein
    >>> class MagnitudeGenerator(object):
    ...     @cachein.Cached()        # () is required!
    ...     def magnitude(self):
    ...         print("CALCULATING")
    ...         return sum(n ** 2 for n in self.terms) ** .5
    ...
    ...     @cachein.CachedAs('terms')
    ...     def get_terms(self):
    ...         return ()
    
    >>> class Vector2D(MagnitudeGenerator):
    ...     def __init__(self, x, y):
    ...         self.x = x
    ...         self.y = y
    ...
    ...     def get_terms(self):
    ...         return (self.x, self.y)
    
    >>> v2d = Vector2D(3, 4)
    >>> v2d.magnitude
    CALCULATING
    5.0
    >>> v2d.magnitude
    5.0
    
    >>> class Vector3D(MagnitudeGenerator):
    ...     def __init__(self, x, y, z):
    ...         self.x = x
    ...         self.y = y
    ...         self.z = z
    ...
    ...     def get_terms(self):
    ...         return (self.x, self.y, self.z)
    
    >>> v3d = Vector3D(3, 4, 5)
    >>> round(v3d.magnitude, 3)
    CALCULATING
    7.071
    >>> round(v3d.magnitude, 3)
    7.071
    
    '''
    
    def __init__(self, name, **_kw):
        super().__init__(name=name, **_kw)
    
    def init(self, method=None, **_kw):
        super().init(**_kw)
        self.method = method
    
    def adopt(self, fn, **_kw):
        return super().adopt(fn, method=fn.__name__, **_kw)

    def __set_name__(self, target, name):
        # name os the name of the method we decorated.  self.name is the name
        # of the attribute that should contain the cache.
        setattr(target, name, self.fn)
        setattr(target, self.name, self)
            
    def getter(self):
        def method_getter(prop, target, cls=None, name=self.name, method=self.method):
            if target is None:      
                return self         # (NO-COV)
            else:
                obj = getattr(target, method)()
                target.__dict__[name] = obj
                return obj
        return method_getter
