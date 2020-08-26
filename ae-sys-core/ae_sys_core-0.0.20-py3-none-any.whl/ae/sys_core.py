"""
dynamic system configuration, initialization and connection
===========================================================

This module allows the dynamic (data-driven) configuration and connection of your application
to all their needed external systems (like servers, databases, cloud stores, ...).


system classes
--------------

The :class:`SystemBase` class represents a single system. The creation of instances of
this class is automatically done :ref:`dynamically <system-properties>` by the
(mostly unique) instance of the class :class:`UsedSystems`.

Each instance of :class:`SystemBase` is using a system-specific connector class for
to establish an internal connection to the represented system. For the implementation of
a connector class, simply inherit from the abstract base class
:class:`SystemConnectionBase` - also provided by this module.

By creating an instance of the class :class:`UsedSystems` you get a dictionary-like
object with all the properties for each configured system. The items of this dict
are instances of the class :class:`SystemBase`.


.. _system-properties:

dynamic system properties
.........................

The properties of your systems are specified within config :ref:`files <config files>`
as :ref:`variables <config-variables>`.

The only mandatory config variable is a dict with the name `availableSystems`, with the system-ids
as dict keys. The items of this dict are also dicts with string keys and called `system configs`.
Only the key `name` is mandatory in these system configs.
The following system config dict keys are supported:

* **name** : system name (long name of system-id, only used for repr() and debugging).
* **credential_keys** : List[str] of credential keys needed for to connect to this system.
* **feature_keys** : List[str] of feature keys supported by this system.
* **available_rec_types** : Dict[str, str] of supported rec type ids and names.
* **connector_module** : name of the connector package.module (def=ae.sys_data_<system-id-in-lower-case>).
* **connector_class** : name of the connector class (def=<system-id>SysConnector),

The value of each credential and feature key gets automatically dynamically read from a config option or
variable. The name of these config options/variables consists of the key string, prefixed with the system id in
lower case. So if e.g. the value of a credential key 'User' for the system id 'Abc' will be
loaded from a config variable with the name `abcUser`. All the credential and feature config
variables can be either stored in the main or the systems section of the config files - see
also :func:`config_value`.

An example of a system configuration you find in the config file `test.cfg`, situated in the
tests folder of this package.


multiple system configurations
..............................

For to provide multiple system configurations for the same application (suite) you can use
individual config files for each application instance with a separate config file
(see .sys_env<SYS_ENV_ID>.cfg :ref:`here <config-files>`).
"""
from abc import ABC, abstractmethod
from collections import OrderedDict
import importlib
from typing import Any, Dict, Optional, Sequence, Union, cast

from ae.core import DEBUG_LEVEL_DISABLED, DEBUG_LEVEL_VERBOSE, HIDDEN_CREDENTIALS   # type: ignore   # mypy
from ae.console import ConsoleApp                               # type: ignore   # mypy doesn't find namespace pkg


__version__ = '0.0.20'


SYS_SECTION_NAME = 'aeSystems'                  #: section name for system config variables


def config_value(var_name: str, console_app: ConsoleApp) -> Any:
    """ determine system configuration setting value from application config options/variables.

    :param var_name:        config variable name. Variable value gets searched in the application instance environment,
                            first in the :ref:`application config options <config-options>`,
                            then in the :ref:`application config variables <config-variables>` (first within
                            the section MAIN_SECTION_NAME/aeOptions and then within SYS_SECTION_NAME/aeSystems.
    :param console_app:     ConsoleApp instance of the application providing these config options/variables.
    :return:                config variable value if found else None.
    """
    val = console_app.get_var(var_name)
    if val is None:
        val = console_app.get_var(var_name, section=SYS_SECTION_NAME)
    return val


class SystemBase:
    """ instance represents an external system, including their system properties and a connection object. """
    instances: int = 0

    def __init__(self, sys_id: str, console_app: ConsoleApp, credentials: Dict[str, str], features: Sequence[str] = (),
                 rec_types: Optional[Dict[str, str]] = None):
        """ create new :class:`SystemBase` instance.

        :param sys_id:      unique str for to identify a system (also used as prefix/suffix).
        :param console_app: ConsoleApp instance of the application using these systems.
        :param credentials: dict for to access system, containing e.g. user name, password, token, dsn...
        :param features:    optional list with special features for this system (see SDF_* constants).
        :param rec_types:   optional dict of available record types for this system.
        """
        self.sys_id = sys_id                            #: system id
        self.console_app = console_app                  #: application instance and config environment
        self.credentials = credentials                  #: credentials for to connect to this system
        self.features = features                        #: system specific features and configs
        self.available_rec_types: Dict[str, str] = \
            rec_types or dict()                         #: record types available in this system

        self.connection: Any = None                     #: object with opt. connect() and disconnect()/close() methods
        self.conn_error: str = ""                     #: error message of last system access or dis-/connect

        SystemBase.instances += 1

    def __repr__(self) -> str:
        """ representation string of this :class:`SystemBase` instance.

        :return: representation string of this instance.
        """
        ret = self.sys_id
        if self.conn_error:
            ret += "!" + self.conn_error
        if self.console_app.debug_level != DEBUG_LEVEL_DISABLED:
            cre = self.credentials
            ret += "&" + repr(cre if self.console_app.debug_level >= DEBUG_LEVEL_VERBOSE else
                              {k: v for k, v in cre.items() if k.lower() not in HIDDEN_CREDENTIALS})
            ret += "_" + repr(self.features)
            ret += "@" + repr(self.console_app.app_name)
        return ret

    def connect(self, sys_config: Dict[str, str], force_reconnect: bool = False) -> str:
        """ connect this instance to his system using a system connector class.

        :param sys_config:          dict with the :ref:`dynamic config properties of this system <system-properties>`.
        :param force_reconnect:     optional; pass True to force re-connection (even if self.connection is
                                    already initialized).
        :return:                    error message or empty string in case of no errors while re-connecting.
        """
        self.conn_error = ""
        if not self.connection or force_reconnect:
            mod_name = sys_config.get('connector_module', 'ae.sys_core_' + self.sys_id.lower())
            connector_module = importlib.import_module(mod_name)
            cls_name = sys_config.get('connector_class', self.sys_id + 'SysConnector')
            connector_class = getattr(connector_module, cls_name)

            self.connection = connector_class(self)
            if self.connection and callable(getattr(self.connection, 'connect', False)):
                self.conn_error = self.connection.connect()
                if self.conn_error:
                    self.connection = None
        return self.conn_error

    def disconnect(self) -> str:
        """ disconnect this external system.

        :return:            error message string or empty string if no errors occurred on disconnection.
        """
        err_msg = ""
        if self.connection:
            if callable(getattr(self.connection, 'disconnect', False)):
                err_msg = self.connection.disconnect()
            elif callable(getattr(self.connection, 'close', False)):
                err_msg = self.connection.close()
            self.connection = None
        self.conn_error = err_msg
        return err_msg


class SystemConnectorBase(ABC):
    """ abstract system connector base class - sub-class establishes the connection to an external system. """
    instances: int = 0

    def __init__(self, system: SystemBase):
        """ create new :class:`SystemBase` instance.

        :param system:      instance of :class:`SystemBase` class that is representing the system using this connection.
        """
        self.system = system                    #: SystemBase instance
        self.console_app = system.console_app   #: application instance and config environment
        self.last_err_msg: str = ""             #: last system connection error message(s)

        SystemConnectorBase.instances += 1

    def __repr__(self) -> str:
        """ representation string of this :class:`SystemBase` instance.

        :return: representation string of this instance.
        """
        ret = self.system.sys_id
        if self.last_err_msg:
            ret += "!" + self.last_err_msg
        if self.console_app.debug_level != DEBUG_LEVEL_DISABLED:
            cre = self.system.credentials
            ret += "&" + repr(cre if self.console_app.debug_level >= DEBUG_LEVEL_VERBOSE else
                              {k: v for k, v in cre.items() if k.lower() not in HIDDEN_CREDENTIALS})
            ret += "_" + repr(self.system.features)
            ret += "@" + repr(self.console_app.app_name)
        return ret

    @abstractmethod
    def connect(self) -> str:
        """ abstract method - raising NotImplementedError, so has to be implemented by the sub-class. """


class UsedSystems(OrderedDict):
    """ An instance of this class is keeping a dictionary of all the found and used systems of this application.

    The keys of this dictionary-like class are the system ids of your application. The items are instances
    of the :class:`SystemBase` class.

    Each instance is providing additionally the following instance attributes:

    * *console_app* - instance of the :class:`~.console.ConsoleApp` class that is using these systems.
    * *available_systems* - system properties loaded from config files.

    All the system-specific properties are stored within the :class:`SystemBase` instances.
    """
    def __init__(self, console_app: ConsoleApp, *selected_systems: str, **entered_credentials: str):
        """ create new instance of :class:`UsedSystems`.

        :param console_app:             ConsoleApp instance of the application using these systems.
        :param selected_systems:        optional iterable of system id strings of the available systems that have to be
                                        initialized for the app specified by the :paramref:`~UsedSystems.console_app`
                                        argument. If no system id get passed then all available systems will be
                                        initialized from the config variable `availableSystems`.
        :param entered_credentials:     optional dict of credentials entered by a user at run-time (overwriting
                                        the values set in the related config variable `availableSystems`).
                                        The keys of this dictionary starting with the system id in lower case,
                                        followed by one of the key strings specified in the **credential_keys** config
                                        list (see :ref:`system-properties`).
        """
        super().__init__()
        self._systems = self

        self.console_app = console_app

        conf_systems = config_value('availableSystems', self.console_app)
        if not conf_systems:
            # noinspection PyProtectedMember
            self.console_app.po(f"****  UsedSystems don't found the 'availableSystems' option or config variable"
                                f"in the config files ({self.console_app._cfg_files})")
            return
        self.available_systems: Dict[str, Dict[str, Union[Dict[str, str], str]]]
        if selected_systems:
            self.available_systems = {k: v for k, v in conf_systems.items() if k in selected_systems}
        else:
            self.available_systems = conf_systems

        self._load_merge_cred_feat(entered_credentials)

    def _load_merge_cred_feat(self, entered_credentials: Dict[str, str]):
        """ load and initialize all used system configs and merge entered credentials into it.

        :param entered_credentials:     passed over unchanged from :class:`UsedSystems` - see
                                        :paramref:`~UsedSystems.entered_credentials`.
        """
        debug_level = self.console_app.debug_level
        for sys_id, sys_config in self.available_systems.items():
            self.console_app.po(f"###   Loading configuration of {sys_config.get('name')} system ({sys_id})...")
            credentials = dict()
            for cred_key in sys_config.get('credential_keys', ()):
                cred_var = sys_id.lower() + cred_key
                found_cred = entered_credentials.get(cred_var, config_value(cred_var, self.console_app))
                if found_cred is None:
                    self.console_app.po(f"***   Ignoring system {sys_id}; credential {cred_var} undefined/incomplete")
                    break  # ignore/skip not fully specified system - continue with next available system
                credentials[cred_key] = found_cred
                if debug_level > DEBUG_LEVEL_DISABLED:
                    if debug_level < DEBUG_LEVEL_VERBOSE and cred_key.lower() in HIDDEN_CREDENTIALS:
                        found_cred = "<hidden>"
                    self.console_app.po(f"..    found credential {cred_var}={found_cred}")
            else:
                # now collect features for this system with complete credentials
                features = list()
                for feat_key in sys_config.get('feature_keys', ()):
                    feat_var = sys_id.lower() + feat_key
                    found_feat = config_value(feat_var, self.console_app)
                    if found_feat:
                        feat_key += '=' + str(found_feat)
                        features.append(feat_key)
                        if debug_level > DEBUG_LEVEL_DISABLED:
                            self.console_app.po(f"..    found feature {feat_var}={found_feat}")
                # finally add system to this used systems instance
                self._add_system(sys_id, credentials, features=features)

    def _add_system(self, sys_id: str, credentials: Dict[str, str], features: Sequence[str] = ()):
        """ add new :class:`SystemBase` instance to this :class:`UsedSystems` instance.

        :param sys_id:                  system id.
        :param credentials:             credentials of the new system to add.
        :param features:                optional list with special features for this system (see SDF_* constants).
        """
        assert sys_id in self.available_systems, f"UsedSystems._add_system(): unsupported system id {sys_id}"
        assert sys_id not in self._systems, f"UsedSystems._add_system(): system id {sys_id} already specified"
        rec_types = cast(Optional[Dict[str, str]], self.available_systems[sys_id].get('available_rec_types'))
        self._systems[sys_id] = SystemBase(sys_id, self.console_app, credentials, features, rec_types)

    def connect(self, force_reconnect: bool = False) -> str:
        """ connect all the selected systems of this instance.

        :param force_reconnect: optional; pass True to force re-connection (even if self.connection is initialized).
        :return:                error message or empty string in case of no errors while re-connecting.
        """
        errors = list()
        for sys_id, system in self._systems.items():
            assert sys_id in self.available_systems, f"sys_config for system {sys_id} missing"
            if system.connect(self.available_systems[sys_id], force_reconnect=force_reconnect)\
                    or not system.connection:
                errors.append(system.conn_error or f"{sys_id} connection failed")
        if errors:
            errors.insert(0, f"####  UsedSystems.connect({force_reconnect}):")
        return "\n   #  ".join(errors)

    def disconnect(self) -> str:
        """ disconnect all available and already connected systems.

        :return:                error message string or empty string if no errors occurred on disconnection.
        """
        errors = list()
        for system in self._systems.values():
            err_msg = system.disconnect()
            if err_msg:
                errors.append(err_msg)
        return "\n   #  ".join(["####  UsedSystems.disconnect():"] + errors) if errors else ""
