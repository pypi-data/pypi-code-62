class SocketException(OSError):
    pass

class IPError(SocketException):
    pass

class PortError(SocketException):
    pass
