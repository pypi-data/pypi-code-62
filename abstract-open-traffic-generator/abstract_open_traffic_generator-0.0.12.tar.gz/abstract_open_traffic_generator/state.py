

class Config(object):
    """State.Config class

    placeholder

    Args
    ----
    - state (Union[str, type(None)]): A request to the traffic generator. CREATE will overwrite any configuration content on the traffic  generator with the payload content. UPDATE will update the current configuration content on the traffic  generator with the payload content. The content MUST be the entire configuration. The traffic generator receiving the configuration must resolve any changes in the submitted configuration. Deleting items from the configuration is an UPDATE with any items are to be deleted missing from the payload content.
    - ports (Union[list[Union[Port, type(None)]], type(None)]): The ports that will be configured on the traffic generator.
    - devices (Union[list[Union[DeviceGroup, type(None)]], type(None)]): The devices that will be configured on the traffic generator.
    - flows (Union[list[Union[Flow, type(None)]], type(None)]): The flows that will be configured on the traffic generator.
    - captures (Union[list[Union[Capture, type(None)]], type(None)]): The captures that will be configured on the traffic generator.
    """
    def __init__(self, state=None, ports=None, devices=None, flows=None, captures=None):
        if isinstance(state, (str, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str, type(None))')
        if isinstance(ports, (list, type(None))) is True:
            self.ports = ports
        else:
            raise TypeError('ports must be an instance of (list, type(None))')
        if isinstance(devices, (list, type(None))) is True:
            self.devices = devices
        else:
            raise TypeError('devices must be an instance of (list, type(None))')
        if isinstance(flows, (list, type(None))) is True:
            self.flows = flows
        else:
            raise TypeError('flows must be an instance of (list, type(None))')
        if isinstance(captures, (list, type(None))) is True:
            self.captures = captures
        else:
            raise TypeError('captures must be an instance of (list, type(None))')


class Flow(object):
    """State.Flow class

    Request for the traffic generator to move flows to a specific state.

    Args
    ----
    - state (Union[str, type(None)]): The requested state of the flows.
    - flows (Union[list[Union[str, type(None)]], type(None)]): The unique names of flow objects.
    """
    def __init__(self, state=None, flows=None):
        if isinstance(state, (str, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str, type(None))')
        if isinstance(flows, (list, type(None))) is True:
            self.flows = flows
        else:
            raise TypeError('flows must be an instance of (list, type(None))')


class Port(object):
    """State.Port class

    Request for the traffic generator to move ports to a specific state.

    Args
    ----
    - state (Union[str, type(None)]): The requested state of the port.
    - ports (Union[list[Union[str, type(None)]], type(None)]): The unique names of port objects.
    """
    def __init__(self, state=None, ports=None):
        if isinstance(state, (str, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str, type(None))')
        if isinstance(ports, (list, type(None))) is True:
            self.ports = ports
        else:
            raise TypeError('ports must be an instance of (list, type(None))')


class Device(object):
    """State.Device class

    Request for the traffic generator to move emulated devices to a specific state.

    Args
    ----
    - state (Union[str, type(None)]): The requested state of the devices.
    - devices (Union[list[Union[str, type(None)]], type(None)]): The unique names of emulated device objects.
    """
    def __init__(self, state=None, devices=None):
        if isinstance(state, (str, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str, type(None))')
        if isinstance(devices, (list, type(None))) is True:
            self.devices = devices
        else:
            raise TypeError('devices must be an instance of (list, type(None))')


class Capture(object):
    """State.Capture class

    Request for the traffic generator to move capture to a specific state.

    Args
    ----
    - state (Union[str, type(None)]): TBD
    - captures (Union[list[Union[str, type(None)]], type(None)]): The unique names of capture objects.
    """
    def __init__(self, state=None, captures=None):
        if isinstance(state, (str, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str, type(None))')
        if isinstance(captures, (list, type(None))) is True:
            self.captures = captures
        else:
            raise TypeError('captures must be an instance of (list, type(None))')


class Desired(object):
    """State.Desired class

    The desired state of the traffic generator 

    Args
    ----
    - choice (Union[str, type(None)]): TBD
    """
    _CHOICE_MAP = {
        'Config': 'config',
        'Port': 'port',
        'Device': 'device',
        'Flow': 'flow',
        'Capture': 'capture',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.state import Config
        from abstract_open_traffic_generator.state import Port
        from abstract_open_traffic_generator.state import Device
        from abstract_open_traffic_generator.state import Flow
        from abstract_open_traffic_generator.state import Capture
        if isinstance(choice, (Config, Port, Device, Flow, Capture)) is False:
            raise TypeError('choice must be of type: Config, Port, Device, Flow, Capture')
        self.__setattr__('choice', Desired._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Desired._CHOICE_MAP[type(choice).__name__], choice)


class Current(object):
    """State.Current class

    The desired and actual state of the traffic generator

    Args
    ----
    - states (Union[str, type(None)]): TBD
    - flow (Union[list[Union[str, type(None)]], type(None)]): A list of configured flow names If the list is empty the type will apply to all configured flows
    - capture (Union[float, int, type(None)]): The number of seconds to wait for all the flows to be in the specified state
    """
    def __init__(self, states=None, flow=None, capture=None):
        if isinstance(states, (str, type(None))) is True:
            self.states = states
        else:
            raise TypeError('states must be an instance of (str, type(None))')
        if isinstance(flow, (list, type(None))) is True:
            self.flow = flow
        else:
            raise TypeError('flow must be an instance of (list, type(None))')
        if isinstance(capture, (float, int, type(None))) is True:
            self.capture = capture
        else:
            raise TypeError('capture must be an instance of (float, int, type(None))')
