

class Port(object):
    """Generated from OpenAPI #/components/schemas/Port.Port model

    An abstract test port used to associate a unique name with the location of a physical or virtual test location. Some different types of test locations are:   
     physical appliance with multiple ports   
     physical chassis with multiple cards and ports   
     local interface   
     virtual machine, docker container, kubernetes cluster  The test port format is implementation specific. Use the /results API to determine what formats the implementation  supports for the location property.

    Args
    ----
    - name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - location (Union[str, type(None)]): The location of the test port.
    - link_state (Union[str, type(None)]): The configured link state of the port. Compare the actual state vs the configured state by using the  /results API.
    - capture_state (Union[str, type(None)]): The configured capture state of the port. Compare the actual state vs the configured state by using the  /results API.
    """
    def __init__(self, name=None, location=None, link_state=None, capture_state=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(location, (str, type(None))) is True:
            self.location = location
        else:
            raise TypeError('location must be an instance of (str, type(None))')
        if isinstance(link_state, (str, type(None))) is True:
            self.link_state = link_state
        else:
            raise TypeError('link_state must be an instance of (str, type(None))')
        if isinstance(capture_state, (str, type(None))) is True:
            self.capture_state = capture_state
        else:
            raise TypeError('capture_state must be an instance of (str, type(None))')
