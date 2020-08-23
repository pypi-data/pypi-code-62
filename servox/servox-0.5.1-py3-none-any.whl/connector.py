from __future__ import annotations
import asyncio
import abc
import importlib
import re
from pathlib import Path
from pkg_resources import EntryPoint, iter_entry_points
from typing import (
    Any,
    ClassVar,
    IO,
    Generator,
    Optional,
    Set,
    Type,
    Tuple,
    get_type_hints,
)

import loguru
from pydantic import (
    BaseModel,
    HttpUrl,
    root_validator,
    validator,
)


from servo import api, events, logging, repeating
from servo.configuration import AbstractBaseConfiguration, BaseConfiguration, Optimizer
from servo.events import EventHandler, EventResult
from servo.types import *
from servo.utilities import (
    OutputStreamCallback,
    SubprocessResult,
    Timeout,
    run_subprocess_shell, 
    stream_subprocess_shell
)


_connector_subclasses: Set[Type["BaseConnector"]] = set()


# NOTE: Initialize mixins first to control initialization graph
class BaseConnector(api.Mixin, events.Mixin, logging.Mixin, repeating.Mixin, BaseModel, abc.ABC, metaclass=events.Metaclass):
    """
    Connectors expose functionality to Servo assemblies by connecting external services and resources.
    """
    
    ##
    # Connector metadata

    name: str = None
    """Name of the connector, by default derived from the class name.
    """

    full_name: ClassVar[str] = None
    """The full name of the connector for referencing it unambiguously.
    """

    version: ClassVar[Version] = None
    """Semantic Versioning string of the connector.
    """

    description: ClassVar[Optional[str]] = None
    """Optional textual description of the connector.
    """

    homepage: ClassVar[Optional[HttpUrl]] = None
    """Link to the homepage of the connector.
    """

    license: ClassVar[Optional[License]] = None
    """An enumerated value that identifies the license that the connector is distributed under.
    """

    maturity: ClassVar[Optional[Maturity]] = None
    """An enumerated value that identifies the self-selected maturity level of the connector, provided for
    advisory purposes.
    """

    ##
    # Instance configuration

    optimizer: Optional[Optimizer]
    """Name of the command for interacting with the connector instance via the CLI.

    Note that optimizers are attached as configuration to Connector instance because
    the settings are not managed as part of the assembly config files and are always
    provided via environment variablesm, commandline arguments, or secrets management.
    """

    config: BaseConfiguration
    """Configuration for the connector set explicitly or loaded from a config file.
    """

    ##
    # Validators

    @root_validator(pre=True)
    @classmethod
    def validate_metadata(cls, v):
        assert cls.name is not None, "name must be provided"
        assert cls.version is not None, "version must be provided"
        if isinstance(cls.version, str):
            # Attempt to parse
            cls.version = Version.parse(cls.version)
        assert isinstance(
            cls.version, Version
        ), "version is not a semantic versioning descriptor"
        
        if not cls.__default_name__:
            if name := _name_for_connector_class(cls):
                cls.__default_name__ = name
            else:
                raise ValueError(f"A default connector name could not be constructed for class '{cls}'")
        return v

    @validator("name")
    @classmethod
    def validate_name(cls, v):
        assert bool(
            re.match("^[0-9a-zA-Z-_/\\.]{3,128}$", v)
        ), "names may only contain alphanumeric characters, hyphens, slashes, periods, and underscores"
        return v

    @classmethod
    def config_model(cls) -> Type["BaseConfiguration"]:
        """
        Return the configuration model backing the connector. 
        
        The model is determined by the type hint of the `configuration` attribute
        nearest in definition to the target class in the inheritance hierarchy.
        """
        hints = get_type_hints(cls)
        config_cls = hints["config"]
        return config_cls

    def __init_subclass__(cls: Type['BaseConnector'], **kwargs):
        super().__init_subclass__(**kwargs)

        _connector_subclasses.add(cls)
        
        cls.name = cls.__name__.replace("Connector", "")
        cls.full_name = cls.__name__.replace("Connector", " Connector")
        cls.version = Version.parse("0.0.0")
        cls.__default_name__ = _name_for_connector_class(cls)

    def __init__(
        self,
        *args,
        name: Optional[str] = None,
        **kwargs,
    ):
        name = (
            name if name is not None else self.__class__.__default_name__
        )
        super().__init__(
            *args, name=name, **kwargs,
        )

    def __hash__(self):
        return hash((self.name, id(self),))
    
    ##
    # Subprocess utilities

    async def run_subprocess(
        self,
        cmd: str,
        *,
        env: Optional[Dict[str, str]] = None,
        timeout: Timeout = None,
        logger: Optional[loguru.Logger] = ...,
        stdin: Union[int, IO[Any], None] = None,
        **kwargs
    ) -> SubprocessResult:
        """
        Run a shell command in a subprocess asynchronously and return the results.

        This method is a convenience wrapper for lower-level functionality implemented in the
        `servo.utilities.subprocess` module. Additional arguments are available for input via
        `kwargs` that have been omitted for brevity to optimize the public API for common cases.

        :param cmd: The command to run.
        :param env: An optional dictionary of environment variables to apply to the subprocess.
        :param timeout: An optional timeout in seconds for how long to read the streams before giving up.
        :param logger: The logger to log messages about the subprocess execution against. Defaults to `self.logger`. `None` disables logging output.
        :param stdin: A file descriptor, IO stream, or None value to use as the standard input of the subprocess. Default is `None`.

        :raises asyncio.TimeoutError: Raised if the timeout expires before the subprocess exits.
        :return: A named tuple value of the exit status and two string lists of standard output and standard error.
        """
        logger_: Optional[loguru.Logger] = self.logger if logger == ... else logger
        try:
            start = time.time()
            if logger_:
                timeout_note = f" ({Duration(timeout)} timeout)" if timeout else ""
                logger_.info(f"Running subprocess command `{cmd}`{timeout_note}")
            result = await run_subprocess_shell(
                cmd,           
                env=env,
                timeout=timeout,
                stdin=stdin,
                **kwargs
            )
            end = time.time()
            duration = Duration(end - start)
            if logger_:
                logger_.info(f"Subprocess finished with return code {result.return_code} in {duration} (`{cmd}`)")
            return result
        except asyncio.TimeoutError as error:
            if logger_:
                logger_.warning(f"timeout expired waiting for subprocess to complete: {error}")
            raise error

    async def stream_subprocess_output(
        self,
        cmd: str,
        *,
        stdout_callback: Optional[OutputStreamCallback] = None,
        stderr_callback: Optional[OutputStreamCallback] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Timeout = None,        
        stdin: Union[int, IO[Any], None] = None,
        logger: Optional[loguru.Logger] = ...,
        **kwargs
    ) -> int:
        """
        Run a shell command in a subprocess asynchronously and stream its output.

        This method is a convenience wrapper for lower-level functionality implemented in the
        `servo.utilities.subprocess` module. Additional arguments are available for input via
        `kwargs` that have been omitted for brevity to optimize the public API for common cases.

        :param cmd: The command to run.
        :param stdout_callback: An optional callable invoked with each line read from stdout. Must accept a single string positional argument and returns nothing.
        :param stderr_callback: An optional callable invoked with each line read from stderr. Must accept a single string positional argument and returns nothing.
        :param env: An optional dictionary of environment variables to apply to the subprocess.
        :param timeout: An optional timeout in seconds for how long to read the streams before giving up.
        :param logger: The logger to log messages about the subprocess execution against. Defaults to `self.logger`. `None` disables logging output.
        :param stdin: A file descriptor, IO stream, or None value to use as the standard input of the subprocess. Default is `None`.

        :raises asyncio.TimeoutError: Raised if the timeout expires before the subprocess exits.
        :return: The exit status of the subprocess.
        """
        logger_: Optional[loguru.Logger] = self.logger if logger == ... else logger
        try:
            start = time.time()
            if logger_:
                timeout_note = f" ({Duration(timeout)} timeout)" if timeout else ""
                logger_.info(f"Running subprocess command `{cmd}`{timeout_note}")
            result = await stream_subprocess_shell(
                cmd,
                stdout_callback=stdout_callback,
                stderr_callback=stderr_callback,                
                env=env,
                timeout=timeout,
                stdin=stdin,
                **kwargs
            )
            end = time.time()
            duration = Duration(end - start)
            if logger_:
                logger_.info(f"Subprocess finished with return code {result} in {duration} (`{cmd}`)")
            return result
        except asyncio.TimeoutError as error:
            if logger_:
                logger_.warning(f"timeout expired waiting for subprocess to complete: {error}")
            raise error


EventResult.update_forward_refs(BaseConnector=BaseConnector)
EventHandler.update_forward_refs(BaseConnector=BaseConnector)


def metadata(
    name: Optional[Union[str, Tuple[str, str]]] = None,
    description: Optional[str] = None,
    version: Optional[Union[str, Version]] = None,
    *,
    homepage: Optional[Union[str, HttpUrl]] = None,
    license: Optional[Union[str, License]] = None,
    maturity: Optional[Union[str, Maturity]] = None,
):
    """Decorate a Connector class with metadata"""

    def decorator(cls):
        if not issubclass(cls, BaseConnector):
            raise TypeError("Metadata can only be attached to Connector subclasses")

        if name:
            if isinstance(name, tuple):
                if len(name) != 2:
                    raise ValueError(f"Connector names given as tuples must contain exactly 2 elements: full name and alias")
                cls.name, cls.__default_name__ = name                
            else:
                cls.name = name
        if description:
            cls.description = description
        if version:
            cls.version = (
                version if isinstance(version, Version) else Version.parse(version)
            )
        if homepage:
            cls.homepage = homepage
        if license:
            cls.license = license if isinstance(license, License) else License.from_str(license)
        if maturity:
            cls.maturity = maturity if isinstance(maturity, Maturity) else Maturity.from_str(maturity)
        return cls

    return decorator

##
# Utility functions

def _name_for_connector_class(cls: Type[BaseConnector]) -> Optional[str]:
    for name in (cls.name, cls.__name__):
        if not name:
            continue
        name = re.sub(r"Connector$", "", name)
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        if name != "":
            return name
    return None


def _connector_class_from_string(connector: str) -> Optional[Type[BaseConnector]]:
    if not isinstance(connector, str):
        return None

    # Check for an existing class in the namespace
    # FIXME: This symbol lookup doesn't seem solid
    connector_class = globals().get(connector, None)
    try:
        connector_class = (
            eval(connector) if connector_class is None else connector_class
        )
    except Exception:
        pass
    
    if _validate_class(connector_class):
        return connector_class

    # Check if the string is an identifier for a connector
    for connector_class in _connector_subclasses:
        if connector == connector_class.__default_name__ or connector in [
            connector_class.__name__,
            connector_class.__qualname__,
        ]:
            return connector_class

    # Try to load it as a module path
    if "." in connector:
        module_path, class_name = connector.rsplit(".", 1)
        module = importlib.import_module(module_path)
        if hasattr(module, class_name):
            connector_class = getattr(module, class_name)
            if _validate_class(connector_class):
                return connector_class

    return None

def _validate_class(connector: type) -> bool:
    if connector is None or not isinstance(connector, type):
        return False

    if not issubclass(connector, BaseConnector):
        raise TypeError(f"{connector.__name__} is not a Connector subclass")

    return True


#####

ENTRY_POINT_GROUP = "servo.connectors"


class ConnectorLoader:
    """
    Dynamically discovers and loads connectors via Python setuptools entry points
    """

    def __init__(self, group: str = ENTRY_POINT_GROUP) -> None:
        self.group = group

    def iter_entry_points(self) -> Generator[EntryPoint, None, None]:
        yield from iter_entry_points(group=self.group, name=None)

    def load(self) -> Generator[Any, None, None]:
        for entry_point in self.iter_entry_points():
            yield entry_point.resolve()
