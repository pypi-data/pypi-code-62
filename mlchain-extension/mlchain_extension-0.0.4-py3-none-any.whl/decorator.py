from inspect import signature

def post_process(transformer):
    def wrapper(func):
        def f(*args, **kwargs):
            o = func(*args, **kwargs)
            return transformer(o)

        f.__signature__ = signature(func)
        f.__name__ = func.__name__
        return f

    return wrapper

