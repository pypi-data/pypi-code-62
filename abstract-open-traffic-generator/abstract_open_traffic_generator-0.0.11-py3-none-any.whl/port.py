

class Port(object):
    """Port.Port class

    An abstract test port used to associate a unique name with the location of a physical or virtual test location. Some different types of test locations are:   
     physical appliance with multiple ports   
     physical chassis with multiple cards and ports   
     local interface   
     virtual machine or docker container

    Args
    ----
    - name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - location (Union[Location, type(None)]): The location of a test resource.
    """
    def __init__(self, name=None, location=None):
        from abstract_open_traffic_generator.port import Location
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(location, (Location, type(None))) is True:
            self.location = location
        else:
            raise TypeError('location must be an instance of (Location, type(None))')


class Location(object):
    """Port.Location class

    The location of a test resource.

    Args
    ----
    - choice (Union[str, type(None)]): TBD
    - physical (Union[Physical, type(None)]): A physical test port
    - interface (Union[Interface, type(None)]): An local interface test port.
    - virtual (Union[Virtual, type(None)]): A virtual test port.  Characterized as an endpoint consisting of an ip address and port. 
    """
    _CHOICE_MAP = {
        'Physical': 'physical',
        'Interface': 'interface',
        'Virtual': 'virtual',
    }
    def __init__(self, choice):
        from abstract_open_traffic_generator.port import Physical
        from abstract_open_traffic_generator.port import Interface
        from abstract_open_traffic_generator.port import Virtual
        if isinstance(choice, (Physical, Interface, Virtual)) is False:
            raise TypeError('choice must be of type: Physical, Interface, Virtual')
        self.__setattr__('choice', Location._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Location._CHOICE_MAP[type(choice).__name__], choice)


class Physical(object):
    """Port.Physical class

    A physical test port

    Args
    ----
    - address (Union[str, type(None)]): TBD
    - board (Union[float, int, type(None)]): TBD
    - port (Union[float, int, type(None)]): TBD
    - fanout (Union[float, int, type(None)]): TBD
    """
    def __init__(self, address=None, board=None, port=None, fanout=None):
        if isinstance(address, (str, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (str, type(None))')
        if isinstance(board, (float, int, type(None))) is True:
            self.board = board
        else:
            raise TypeError('board must be an instance of (float, int, type(None))')
        if isinstance(port, (float, int, type(None))) is True:
            self.port = port
        else:
            raise TypeError('port must be an instance of (float, int, type(None))')
        if isinstance(fanout, (float, int, type(None))) is True:
            self.fanout = fanout
        else:
            raise TypeError('fanout must be an instance of (float, int, type(None))')


class Interface(object):
    """Port.Interface class

    An local interface test port.

    Args
    ----
    - name (Union[str, type(None)]): TBD
    """
    def __init__(self, name=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')


class Virtual(object):
    """Port.Virtual class

    A virtual test port.  Characterized as an endpoint consisting of an ip address and port. 

    Args
    ----
    - address (Union[str, type(None)]): TBD
    - port (Union[float, int, type(None)]): TBD
    """
    def __init__(self, address=None, port=None):
        if isinstance(address, (str, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (str, type(None))')
        if isinstance(port, (float, int, type(None))) is True:
            self.port = port
        else:
            raise TypeError('port must be an instance of (float, int, type(None))')
