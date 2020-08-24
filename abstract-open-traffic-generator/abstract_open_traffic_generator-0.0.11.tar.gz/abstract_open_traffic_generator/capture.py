

class Capture(object):
    """Capture.Capture class

    Capture model

    Args
    ----
    - name (Union[str, type(None)]): Unique name of an object that is the primary key for objects found in  arrays.
    - ports (Union[list[Union[str, type(None)]], type(None)]): A list of port names to configure capture settings on
    - filters (Union[str, type(None)]): TBD
    """
    def __init__(self, name=None, ports=None, filters=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(ports, (list, type(None))) is True:
            self.ports = ports
        else:
            raise TypeError('ports must be an instance of (list, type(None))')
        if isinstance(filters, (str, type(None))) is True:
            self.filters = filters
        else:
            raise TypeError('filters must be an instance of (str, type(None))')
