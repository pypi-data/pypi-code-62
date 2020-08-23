"""
This module provides implementations to load documentation information from
an identifier as it is specified in the `pydocmd.yml:generate` configuration
key. A loader basically takes care of loading the documentation content for
that name, but is not supposed to apply preprocessing.
"""

from __future__ import print_function

import dataclasses
import inspect
import re
import sys
import types
from typing import Any, Callable, List, Optional, Tuple, Union

from .imp import import_object_with_scope

# Use typing_extensions for Python < 3.8
if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal  # noqa


function_types = (
    types.FunctionType,
    types.LambdaType,
    types.MethodType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
)
if hasattr(types, "UnboundMethodType"):
    function_types += (types.UnboundMethodType,)

# Union[MathyEnvState, NoneType] -> Optional[MathyEnvState]
optional_match = r"(.*)Union\[(.*),\sNoneType\](.*)"
optional_replace = r"\1Optional[\2]\3"

# _ForwardRef('MathyEnvState') -> MathyEnvState
fwd_ref_match = r"(.*)\_?ForwardRef\(\'(.*)\'\)(.*)"
fwd_ref_replace = r"\1\2\3"

FunctionTypes = Union[
    Literal["class"],
    Literal["function"],
    Literal["dataclass"],
    Literal["classmethod"],
    Literal["method"],
]


def cleanup_type(type_string: str) -> str:
    # Optional[T] gets expanded to Union[T, NoneType], so change it back
    while re.search(optional_match, type_string) is not None:
        type_string = re.sub(optional_match, optional_replace, type_string)

    # _ForwardRef('MathyEnvState') -> MathyEnvState
    while re.search(fwd_ref_match, type_string) is not None:
        type_string = re.sub(fwd_ref_match, fwd_ref_replace, type_string)

    return type_string


def trim(docstring):
    if not docstring:
        return ""
    lines = [x.rstrip() for x in docstring.split("\n")]
    lines[0] = lines[0].lstrip()

    indent = None
    for i, line in enumerate(lines):
        if i == 0 or not line:
            continue
        new_line = line.lstrip()
        delta = len(line) - len(new_line)
        if indent is None:
            indent = delta
        elif delta > indent:
            new_line = " " * (delta - indent) + new_line
        lines[i] = new_line

    return "\n".join(lines)


class PythonLoader(object):
    """
  Expects absolute identifiers to import with #import_object_with_scope().
  """

    def __init__(self, config):
        self.config = config

    def load_section(self, section):
        """
    Loads the contents of a #Section. The `section.identifier` is the name
    of the object that we need to load.

    # Arguments
      section (Section): The section to load. Fill the `section.title` and
        `section.content` values. Optionally, `section.loader_context` can
        be filled with custom arbitrary data to reference at a later point.
    """

        assert section.identifier is not None
        obj, scope = import_object_with_scope(section.identifier)

        if "." in section.identifier:
            default_title = section.identifier.rsplit(".", 1)[1]
        else:
            default_title = section.identifier

        section.title = getattr(obj, "__name__", default_title)
        section.content = trim(get_docstring(obj))
        section.loader_context = {"obj": obj, "scope": scope}

        # Add the function signature in a code-block.
        if callable(obj):
            sig, fn_type = get_function_signature(
                obj, scope if inspect.isclass(scope) else None
            )
            section.content = f"```python\n{sig}\n```\n{section.content}"
            section.title = f"{section.title} <kbd>{fn_type}</kbd>"


def get_docstring(function):
    if hasattr(function, "__name__") or isinstance(function, property):
        return function.__doc__ or ""
    elif hasattr(function, "__call__"):
        return function.__call__.__doc__ or ""
    else:
        return function.__doc__ or ""


class CallableArg:
    name: str
    type_hint: Optional[str]
    default: Optional[str]

    def __init__(self, name: str, type_hint: Optional[str], default: Optional[str]):
        self.name = name
        self.type_hint = type_hint
        self.default = default


class CallablePlaceholder:
    simple: str
    name: str
    args: List[CallableArg]
    return_type: Optional[str]
    fn_type: FunctionTypes

    def __init__(
        self,
        simple: str,
        name: str,
        args: List[CallableArg],
        fn_type: FunctionTypes,
        return_type: Optional[Any] = None,
    ):
        self.simple = simple
        self.name = name
        self.args = args
        self.return_type = return_type
        self.fn_type = fn_type


def get_fn_type(function: Any) -> FunctionTypes:
    sig: inspect.Signature = inspect.signature(function)
    is_class = inspect.isclass(function)
    is_method = inspect.ismethod(function)
    is_function = inspect.isfunction(function)
    is_dataclass = dataclasses.is_dataclass(function)
    prms = [p.name for p in list(sig.parameters.values())]
    fn_type: FunctionTypes
    if is_method and not is_function:
        fn_type = "classmethod"
    elif is_dataclass:
        fn_type = "dataclass"
    elif is_method or is_function and len(prms) > 0 and prms[0] == "self":
        fn_type = "method"
    elif is_function:
        fn_type = "function"
    elif is_class:
        fn_type = "class"
    else:
        raise ValueError(f"unknown type of function: {function}")
    return fn_type


def get_callable_placeholder(
    function: Callable, owner_class=None, show_module=False
) -> CallablePlaceholder:
    isclass = inspect.isclass(function)
    orig_fn = function

    # Get base name.
    name_parts = []
    if show_module:
        name_parts.append(function.__module__)
    if owner_class:
        name_parts.append(owner_class.__name__)
    if hasattr(function, "__name__"):
        name_parts.append(function.__name__)
    else:
        name_parts.append(type(function).__name__)
        name_parts.append("__call__")
        function = function.__call__
    if isclass:
        function = getattr(function, "__init__", None)

    name = ".".join(name_parts)
    sig = inspect.signature(function)
    fn_type: FunctionTypes = get_fn_type(orig_fn)

    params = []
    for p in sig.parameters.values():
        annotation = None
        default_value = None
        if p.annotation is not inspect._empty:  # type: ignore
            annotation = inspect.formatannotation(p.annotation)
        if p.default is not inspect._empty:  # type: ignore
            if isinstance(p.default, str):
                default_value = repr(p.default)
            else:
                default_value = str(p.default)
        if annotation is not None:
            annotation = cleanup_type(annotation)
        params.append(CallableArg(p.name, annotation, default_value))

    return_annotation = None
    if sig.return_annotation is not inspect._empty:  # type: ignore
        return_annotation = inspect.formatannotation(sig.return_annotation)
    if return_annotation is not None:
        return_annotation = cleanup_type(return_annotation)
    return CallablePlaceholder(
        simple=str(sig),
        name=name,
        args=params,
        return_type=return_annotation,
        fn_type=fn_type,
    )


def get_function_signature(
    function: Callable,
    owner_class: Optional[Any] = None,
    show_module: bool = False,
    indent: int = 4,
    max_width: int = 82,
) -> Tuple[str, str]:
    """Return a tuple of the function signature and its function type string"""
    placeholder: CallablePlaceholder = get_callable_placeholder(
        function=function, owner_class=owner_class, show_module=show_module
    )

    out_str = placeholder.name + placeholder.simple
    sep = ""
    indent_str = ""
    long_line: bool = len(out_str) >= max_width
    if long_line:
        sep = "\n"
        indent_str = " " * indent

    out_str = f"{placeholder.name}({sep}"
    arg: CallableArg
    for arg in placeholder.args:
        arg_str = f"{indent_str}{arg.name}"
        if arg.type_hint is not None:
            arg_str += f": {arg.type_hint}"
        if arg.default is not None:
            arg_str += f" = {arg.default}"
        arg_str += f", {sep}"
        out_str += arg_str

    # Remove trailing comma on single-line fns
    if not long_line and out_str[-2:] == ", ":
        out_str = out_str[0:-2]
    out_str += ")"
    if placeholder.return_type is not None:
        out_str += f" -> {placeholder.return_type}"

    return out_str, placeholder.fn_type
