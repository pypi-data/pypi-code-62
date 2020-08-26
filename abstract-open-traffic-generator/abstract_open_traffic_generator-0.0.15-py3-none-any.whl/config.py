

class Config(object):
    """Generated from OpenAPI #/components/schemas/Config.Config model

    A container for all models that are part of the configuration
    

    Args
    ----
    - ports (Union[list[Union[Port]], None]): The ports that will be configured on the traffic generator
    - devices (Union[list[Union[DeviceGroup]], None]): The devices that will be configured on the traffic generator
    - flows (Union[list[Union[Flow]], None]): The flows that will be configured on the traffic generator
    - captures (Union[list[Union[Capture]], None]): The captures that will be configured on the traffic generator
    """
    def __init__(self, ports=None, devices=None, flows=None, captures=None):
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
