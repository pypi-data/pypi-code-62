from mlchain.base.serve_model import ServeModel


class MlchainSameResultResponse:
    def __init__(self, task_id):
        self.task_id = task_id


def step(name=None):
    if isinstance(name, (str, type(None))):
        def wrapper(func):
            func.__queue__ = name or func.__qualname__
            return func

        return wrapper
    else:
        name.__queue__ = name.__qualname__
        return name


class QueueModel(ServeModel):
    def __init__(self, model, deny_all_function=False,
                 blacklist=[], whitelist=[]):
        if isinstance(model, ServeModel):
            self.__dict__.update(model.__dict__)
            self.__dir__ = model.__dir__
        else:
            ServeModel.__init__(self, model, deny_all_function=deny_all_function, blacklist=blacklist,
                                whitelist=whitelist)

    def call_async(self, function_name_, key_=None, *args, **kwargs):
        raise NotImplementedError

    def result(self, key):
        raise NotImplementedError

    def get_function(self, function_name):
        if function_name == 'store_get':
            return self.result
        if function_name.endswith('_async'):
            return ServeModel.get_function(self, function_name[:-6])
        else:
            return ServeModel.get_function(self, function_name)

    def call_function(self, function_name_, id_=None, *args, **kwargs):
        function_name, id = function_name_, id_
        if function_name == 'store_get' and len(args) + len(kwargs) == 1:
            return self.result(*args, **kwargs)

        if function_name.endswith('_async'):
            call_async = True
            function_name = function_name[:-6]
        else:
            call_async = False
        if call_async:
            output = self.call_async(function_name, id, *args, **kwargs)
            return output
        else:
            output = ServeModel.call_function(self, function_name, id, *args, **kwargs)
            return output
