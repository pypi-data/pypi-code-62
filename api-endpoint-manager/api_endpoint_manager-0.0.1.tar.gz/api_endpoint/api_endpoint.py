from abc import ABCMeta


class APIEndpoint(metaclass=ABCMeta):
    def __init__(self, api, route, qs_args_def, body_args_def, business_class, authorization_object=None):
        pass
