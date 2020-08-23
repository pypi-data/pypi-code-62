# Author: Jingping.zhao

from flask import request
from flask_restful import Resource

from app import application
from framework.orc import Orc
from framework.lib.OrcString import OrcNameStr
from framework.exception import OrcFrameworkApiException


class OrcBasicApi(Resource):
    """
    Support Post
    Using parameter func as function
    """
    def __init__(self):
        Resource.__init__(self)

        self._resource = None

        proc_name = OrcNameStr().from_module_name(self.__class__.__name__).process_name()
        try:
            self._resource = __import__("process.%s" % proc_name, {}, {}, ["modules"]).__getattribute__(proc_name)()
        except (AttributeError, ImportError):
            application.logger.warning("Import process %s failed!" % proc_name)

    @Orc.api
    def dispatch_request(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        application.logger.info("Received request %s -> %s" % (request.method, request.args))

        if "POST" != request.method:
            raise OrcFrameworkApiException(0x2, "Unsupported method: %s" % request.method)

        if "method" not in request.args:
            raise OrcFrameworkApiException(0x3, "Args 'method' is not found")

        func = getattr(self, request.args["method"], None)

        if func is None:
            raise OrcFrameworkApiException(0x4, "Function %s is not supported" % request.args["method"])

        return func(*args, **kwargs)

    def help(self):
        """
        :return:
        """
        return "Service is empty" if self._funcs is None else "Support functions: %s" % " ".join(self._funcs)

    def post(self):
        """
        :return:
        """
        pass


class OrcApi(OrcBasicApi):
    """
    Single resource operation
    """
    def __init__(self, p_funcs: list = None):
        """
        :param p_funcs:
        """
        OrcBasicApi.__init__(self)

        # Create functions
        self._funcs = p_funcs or ["delete", "update", "query"]
        for _name in self._funcs:
            setattr(self, _name, self._create_func(_name))

    def _create_func(self, p_func):
        """
        :param p_func: func name
        :return:
        """
        def func(resource_id):
            """
            :param resource_id:
            :return:
            """
            parameter = {"id": resource_id}
            parameter.update(request.json)
            resource = getattr(self, "_resource")
            return p_func if resource is None else getattr(resource, p_func)(parameter)

        def delete(resource_id):
            """
            :param resource_id:
            :return:
            """
            parameter = {"id": [resource_id]}
            parameter.update(request.json)
            resource = getattr(self, "_resource")
            return p_func if resource is None else getattr(resource, p_func)(parameter)

        def query(resource_id):
            """
            :param resource_id:
            :return:
            """
            parameter = {"id": resource_id}
            parameter.update(request.json)
            resource = getattr(self, "_resource")
            if resource is None:
                return "Query"
            result = getattr(resource, p_func)(parameter)
            return None if not result else result[0]

        funcs = {
            "query": query,
            "delete": delete
        }
        return func if p_func not in funcs else funcs[p_func]


class OrcListApi(OrcBasicApi):
    """
    Resource list operation
    """
    def __init__(self, p_funcs: list = None):
        OrcBasicApi.__init__(self)

        # Create functions
        self._funcs = p_funcs or ["add", "delete", "query"]
        for _name in self._funcs:
            setattr(self, _name, self._create_func(_name))

    def _create_func(self, p_func):
        """
        :param p_func: func name
        :return:
        """
        def func():
            """
            :return:
            """
            resource = getattr(self, "_resource")
            return p_func if resource is None else getattr(resource, p_func)(request.json)

        return func
