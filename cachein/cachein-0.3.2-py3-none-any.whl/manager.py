from .member import Cached

class CacheManager(object):
    '''
    >>> import cachein
    >>> class Vector(tuple):
    ...     @cachein.Cached()
    ...     def magnitude(self):
    ...         print("CALCULATING")
    ...         return sum(n ** 2 for n in self) ** .5
   
    >>> v = Vector((3, 4))
    >>> cached = CacheManager(v)
    >>> 'magnitude' in cached
    False
    >>> cached.magnitude
    Traceback (most recent call last):
        ...
    AttributeError: magnitude
    
    >>> v.magnitude
    CALCULATING
    5.0
    >>> 'magnitude' in cached
    True
    >>> v.magnitude
    5.0
    >>> cached.magnitude
    5.0
    
    >>> del cached.magnitude
    >>> 'magnitude' in cached
    False
    >>> v.magnitude
    CALCULATING
    5.0
    
    >>> cached['magnitude']
    5.0
    
    >>> del cached['magnitude']
    
    >>> cached['magnitude']
    Traceback (most recent call last):
        ...
    KeyError: 'magnitude'
    >>> cached['magnitude':'MISSING']
    'MISSING'
    
    >>> 'magnitude' in cached
    False
    
    >>> cached.magnitude = 'FAKE!'
    >>> v.magnitude
    'FAKE!'
    >>> cached['magnitude'] = 'ALSO FAKE!'
    >>> v.magnitude
    'ALSO FAKE!'
    
    >>> cached.__len__
    Traceback (most recent call last):
        ...
    ValueError: '__len__' is not a cached attribute.
    
    '''
    
    def __init__(self, cached):
        self.__dict__['__cached__'] = cached
        
    def __getitem__(self, key, Cached=Cached, default=KeyError):
        if type(key) is slice:
            default = key.stop
            key = key.start

        # Even if default is provided, generate KeyError if this isn't even
        # a cachable attribute.
        if not isinstance(getattr(type(self.__cached__), key, None), Cached):
            raise ValueError('%r is not a cached attribute.' % key) # (COV-NO-DT
            
        result = self.__cached__.__dict__.get(key, KeyError)
        if result is not KeyError:
            return result
        elif default is KeyError:
            raise KeyError(key)
        else:
            return default

    def __setitem__(self, key, value, Cached=Cached):
        if not isinstance(getattr(type(self.__cached__), key, None), Cached):
            raise ValueError('%r is not a cached attribute.' % key) # (COV-NO-DT)
        self.__cached__.__dict__[key] = value

    def __delitem__(self, key, Cached=Cached):
        if not isinstance(getattr(type(self.__cached__), key, None), Cached):
            raise ValueError('%r is not a cached attribute.' % key) # (COV-NO-DT
        self.__cached__.__dict__.pop(key, None)

    def __getattr__(self, name, Cached=Cached):
        if not isinstance(getattr(type(self.__cached__), name, None), Cached):
            raise ValueError('%r is not a cached attribute.' % name) # (COV-NO-DT
        try:
            return self.__cached__.__dict__[name]
        except KeyError:
            raise AttributeError(name)
        
    def __setattr__(self, name, value, Cached=Cached):
        if not isinstance(getattr(type(self.__cached__), name, None), Cached):
            raise ValueError('%r is not a cached attribute.' % name) # (COV-NO-DT
        self.__cached__.__dict__[name] = value

    def __delattr__(self, name, Cached=Cached):
        if not isinstance(getattr(type(self.__cached__), name, None), Cached):
            raise ValueError('%r is not a cached attribute.' % name) # (COV-NO-DT
        self.__cached__.__dict__.pop(name, None)
        
    def __contains__(self, name, Cached=Cached):
        if not isinstance(getattr(type(self.__cached__), name, None), Cached):
            raise ValueError('%r is not a cached attribute.' % name) # (COV-NO-DT
        return name in self.__cached__.__dict__

class CacheinClass(object):
    '''
    Provides a __cachein__ CacheManager.  This is optiona and only needed if
    having a __cachein__ property is desried.
    
    >>> import cachein
    >>> class Vector(tuple, cachein.CacheinClass):
    ...     @cachein.Cached()
    ...     def magnitude(self):
    ...         print("CALCULATING")
    ...         return sum(n ** 2 for n in self) ** .5
    
    >>> v = Vector((3, 4))
    >>> 'magnitude' in v.__cachein__
    False
    >>> v.magnitude
    CALCULATING
    5.0
    >>> 'magnitude' in v.__cachein__
    True
    '''
    
    __cachein__ = Cached().adopt(CacheManager)
