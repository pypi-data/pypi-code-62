from elasticapm import Client as APMClient, set_custom_context
from elasticapm.context.contextvars import execution_context
from elasticapm.utils.disttracing import TraceParent
from inspect import signature
from mlchain import mlconfig
from mlchain.base.converter import str2bool
from mlchain import mlchain_context


class Client:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.client_ = APMClient(*args, **kwargs)
        try:
            self.client_.capture_message('ping')
            self.client_._transport.flush()
        except:
            self.client_.close()
            raise ConnectionError("Can't connect to APM-Server")

    @property
    def client(self):
        if self.client_ is None:
            self.client_ = APMClient(*self.args, **self.kwargs)
        return self.client_

    def close(self):
        try:
            self.client_.close()
        except:
            pass
        self.client_ = None

    def end_transaction(self, name=None, result="", duration=None):
        try:
            return self.client.end_transaction(name=name, result=result, duration=duration)
        except:
            self.close()
            return None

    def begin_transaction(self, transaction_type, trace_parent=None, start=None):
        try:
            return self.client.begin_transaction(transaction_type, trace_parent=trace_parent, start=start)
        except:
            self.close()
            return None

    def capture_exception(self, exc_info=None, handled=True, **kwargs):
        try:
            return self.client.capture_exception(exc_info=exc_info, handled=handled, **kwargs)
        except:
            self.close()
            return None

    def __getattr__(self, item):
        attr = getattr(self.client, item)
        return attr


class TraceApm:
    def __init__(self, name=None, trace=None):
        self.name = name or mlconfig.name
        if trace is None:
            trace = mlconfig.trace
        if trace is None:
            self.trace = False
        elif isinstance(trace, str):
            self.trace = str2bool(trace)
        else:
            self.trace = trace
        if self.trace:
            self.client = Client(service_name=self.name)

    def __call__(self, func):
        def f(*args, **kwargs):
            if 'Traceparent' in mlchain_context:
                trace_parent = TraceParent.from_string(mlchain_context['Traceparent'])
            else:
                trace_parent = None
            name = str(func.__name__)
            if self.trace:
                transaction = self.client.begin_transaction(name, trace_parent=trace_parent)
                set_custom_context({'context_id': mlchain_context['context_id']})
                mlchain_context['Traceparent'] = transaction.trace_parent.to_string()
            out = func(*args, **kwargs)
            if self.trace:
                self.client.end_transaction(name)
                mlchain_context.pop('Traceparent')
            return out

        func_signature = signature(func)
        f.__signature__ = func_signature
        f.__name__ = func.__name__
        return f
