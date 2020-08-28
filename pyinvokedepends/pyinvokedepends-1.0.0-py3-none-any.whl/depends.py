from invoke import tasks

import warnings
import os
import glob

def dependens(*args, **kvargs):
    """ . """
    class decorator(tasks.Task):
        """ . """
        def __init__(self, func):
            super().__init__(func)
            self.func = func

        def __call__(self, *args, **kwargs):
            """ . """
            callthetask = True
            checks = [os.path.getmtime(path) for pattern in kvargs['checks'] for path in glob.glob(pattern)]
            if len(checks)==0:
                raise ValueError("none of files in checks exist", kvargs['checks'])
            creates = [os.path.getmtime(path) for pattern in kvargs['creates'] for path in glob.glob(pattern)]
            if len(creates)!=0:
                callthetask = max(checks)>=min(creates)
            if callthetask:
                return self.func(*args, **kwargs)
            print('Not calling {func}'.format(func=self.func.__name__))
            return None

    if len(args)>0:
        if not isinstance(args[0], tasks.Task) or len(args)!=1:
            raise ValueError("@depends only possible with kwargs")
        warnings.warn('@depends without arguments will do nothing', SyntaxWarning)
        kvargs['checks']=['.']
        kvargs['creates']=['.']
        return decorator(args[0])
    n = len({'checks', 'creates'}.intersection(set(kvargs.keys())))
    if n in (2,0):
        if n==0:
            warnings.warn('@depends without "checks" and "creates" will do nothing', SyntaxWarning)
            kvargs['checks']=['.']
            kvargs['creates']=['.']
        return decorator
    raise ValueError('@depends needs both "checks" and "creates"')
