class SpotifyException(Exception):
    """Exception to raise in case something bad happens during request"""
    pass


class ClientException(Exception):
    """Exception to raise in case of error on our end for request"""
