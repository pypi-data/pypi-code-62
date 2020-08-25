"""
Response handler helpers for AWS Lambda
"""
from json import loads
from typing import Tuple, Any

from ckf_api_toolkit.tools.api_response_handler import ApiResponseException, ResponseCode
from ckf_api_toolkit.tools.handler import KwargMapper, ArgMapper
from ckf_api_toolkit.tools.logger import Logger, LogLevel

AWS_BODY_KEY = 'body'
AWS_PATH_PARAMS_KEY = 'pathParameters'


def __get_event_from_args(*args):
    """Return the event from the Lambda handler args

    Args:
        *args: The args to parse

    Returns:
        The Lambda event
    """
    return args[0]


def __get_body(event) -> dict:
    """Get the body from the Lambda event

    Args:
        event (): The event to parse

    Returns:
        (dict) Request body of the event
    """
    if AWS_BODY_KEY not in event and not event[AWS_BODY_KEY]:
        raise ApiResponseException(ResponseCode.BAD_REQUEST, "No request body.")
    try:
        Logger().log(LogLevel.debug, event, title=f"Lambda Event", pretty_json=True)
        return loads(event[AWS_BODY_KEY])
    except TypeError:
        return event[AWS_BODY_KEY]


def __get_path_parameter(event, path_param_name: str) -> str:
    """Return a path parameter based on name from the event

    Args:
        event (): Event to pase
        path_param_name (str): Name of the path parameter to return

    Returns:
        (str) The path parameter value from the given name
    """
    if AWS_PATH_PARAMS_KEY not in event and not event[AWS_PATH_PARAMS_KEY]:
        raise ApiResponseException(ResponseCode.BAD_REQUEST, "No path parameters.")
    Logger().log(LogLevel.debug, event, title=f"Lambda Event", pretty_json=True)
    path_params = event[AWS_PATH_PARAMS_KEY]
    if path_param_name not in path_params:
        raise ApiResponseException(ResponseCode.BAD_REQUEST, f"Missing path parameter '{path_param_name}'.")
    return path_params[path_param_name]


def aws_lambda_body_arg_mapper(*args) -> dict:
    """A mapper for Lambda body args, returning them as a dictionary

    Args:
        *args: The args to parse

    Returns:
        (dict) Lambda body args as a dict
    """
    event = __get_event_from_args(*args)
    return __get_body(event)


def get_aws_lambda_body_kwarg_mapper(kwarg_name: str) -> KwargMapper:
    """Return a mapper for a Lambda body kwarg

    Args:
        kwarg_name (str): The name of the kwarg that will get passed to the handler by this mapper.

    Returns:
        (KwargMapper) The mapper for this kwarg
    """
    def __kwarg_mapper(*args) -> Tuple[str, Any]:
        return kwarg_name, aws_lambda_body_arg_mapper(*args)

    return __kwarg_mapper


def get_aws_lambda_path_param_arg_mapper(path_param_name: str) -> ArgMapper:
    """Return a mapper for a Lambda path parameter arg

    Args:
        path_param_name (str): Name of the path parameter to map

    Returns:
        (ArgMapper) The mapper for this path param arg
    """
    def __arg_mapper(*args) -> Any:
        return __get_path_parameter(__get_event_from_args(*args), path_param_name)

    return __arg_mapper


def get_aws_lambda_path_param_kwarg_mapper(kwarg_name: str, path_param_name: str) -> KwargMapper:
    """Return a mapper for a Lambda path parameter kwarg

    Args:
        kwarg_name (str): The name of the kwarg that will get passed to the handler by this mapper.
        path_param_name (str): Name of the path parameter to map

    Returns:
        (KwargMapper) The mapper for this path param kwarg
    """
    def __kwarg_mapper(*args) -> Tuple[str, Any]:
        return kwarg_name, get_aws_lambda_path_param_arg_mapper(path_param_name)(*args)

    return __kwarg_mapper
