import re
__all__ = ['getIP',
           'isValidIP'
           ]
def getIP():
    return socket.gethostbyname(socket.gethostname())

def isValidIP(ip):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$''' 
    if(re.search(regex, ip)):
        return True              
    return False
