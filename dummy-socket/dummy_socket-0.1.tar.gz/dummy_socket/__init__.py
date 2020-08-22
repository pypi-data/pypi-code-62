import socket
import time
import sys
import re
import pprint
import math
import ssl
from usefullibs.socket.exceptions import *

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`1234567890-=~!@#$%^&*()_+[]\;\';,./:"?><{}|'
__doc__ = 'simple socket programming for dummies.'
__all__ = ['serve_forever(port)',
           'client(host, port, mySocket)',
           'isValidPort(port)',
           'getSocket()',
           'isValidIP(ip)',
           'serve(port, mySockek)',
           'client_forever(host, port, mySocket)',
           'encryptMessage(key, message)',
           'decryptMessage(key, message)'
           ]

def encryptMessage(key, message):
    return _translateMessage(key, message, 'encrypt')

def decryptMessage(key, message):
    return _translateMessage(key, message, 'decrypt')

def _translateMessage(key, message, mode):
    translated = [] # Stores the encrypted/decrypted message string.

    keyIndex = 0
    key = key.upper()

    for symbol in message: # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1 means symbol.upper() was not found in LETTERS.
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) # Add if encrypting.
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) # Subtract if decrypting.
            num %= len(LETTERS) # Handle any wraparound.

            # Add the encrypted/decrypted symbol to the end of translated:
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1 # Move to the next letter in the key.
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Append the symbol without encrypting/decrypting.
            translated.append(symbol)

    return ''.join(translated)

def getAll():
    pprint.pprint(__all__)
def getSocket():
    mySocket = socket.socket()
    return mySocket

def isValidPort(port):
    if (port < 65535) and (port >0):
        return True
    return False

def isValidIP(ip):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$''' 
    if(re.search(regex, ip)):
        return True              
    return False

def serve(port, socket1, key，advanced_encryption=True):
    s = secureID
    host = socket.gethostbyname(socket.gethostname())
    if advanced_encryption:
        mySocket = ssl.wrap_socket(socket1, ssl_version=ssl.PROTOCOL_TLS, ciphers="ADH-AES256-SHA")
    else:
        mySocket = socket1
    if not isValidPort(port):
        print('Port is invalid.\nPort set to defaut value.')
        port = 35692
    print('Creating Server...')
    try:
        mySocket.bind((host,port))
    except Exception as err:
        sys.exit('there was an error:', err)
    print('Server created using IP Address {}, Port {}.'.format(host, str(port)))
    print('Server listening....')
    mySocket.listen()
    
    conn, addr = mySocket.accept()
    print("Connection from: " + str(addr))
    
    while True:
        data = decryptMessage(key, conn.recv(8192).decode())
        if data == 'exit()':
            break
        print ("From Connected User " + conn + ' ' + addr + ": " + str(data))

        data = str(data).upper()
        data = input("-->")
        if data == 'exit()':
            break
        data = encryptMessage(key, data)
        conn.send(data.encode())                                                    
    conn.close()


def serve_forever(port, socket1, key, advanced_encryption=True):
    host = socket.gethostname()
    if advanced_encryption:
        mySocket = ssl.wrap_socket(socket1, ssl_version=ssl.PROTOCOL_TLS, ciphers="ADH-AES256-SHA")
    else:
        mySocket = socket1
    if not isValidPort(port):
        print('port is invalid.\nport set to defaut value.', file=sys.stderr)
        port = 35692
    print('Creating Server...')
    try:
        mySocket.bind((host,port))
    except Exception as err:
        sys.exit('there was an error:', err)
    print('Server created using IP Address {}, Port {}.'.format(host, str(port)))
    print('Server listening....')
    mySocket.listen()
    while True:
        conn, addr = mySocket.accept()
        print ("Connection from: " + str(addr))

        while True:
            data = conn.recv(e4096).decode()
            data = decryptMessage(key, data)
            if data == 'exit()':
                break
            print ("From Connected User: " + str(data))

            data = input("-->")
            if data == 'exit()':
                break
            conn.send(encryptMessage(key, data).encode())
        keepgoing = input('enter to continue, anything else to stop: ')
        if keepgoing != '':
            break
        print('Server listening....')
                                                    
    conn.close()
                
def client(host, port, socket, key, advanced_encryption=True):
    x = 1
    print('trying to connect to', host, '...')
    socket.settimeout(50)
    if advanced_encryption:
        mySocket = ssl.wrap_socket(socket1, ssl_version=ssl.PROTOCOL_TLS, ciphers="ADH-AES256-SHA")
    else:
        mySocket = socket1
    while True:
        try:
            mySocket.connect((host,port))
            break
        except OSError:
            x += 1
            if x == 100000000000:
                print('socket timeout', file=sys.stderr)
                sys.exit()
            pass
        except socket.timeout:
            print('socket timeout', file=sys.stderr)
            sys.exit()

    print('got connection from', host, ', port', str(port))
    message = input("-->")

    while message != 'exit()':
        mySocket.send(encryptMessage(key, message).encode())
        data = decryptMessage(key, mySocket.recv(4096).decode())
        print ('Received from server: ' + data)
        message = input("-->")

    mySocket.close()

def client_forever(host, port, mySocket, advanced_encryption=True):
    a_e = advanced_encryption
    while True:
        client(host, port, mysocket, advanced_encryption=a_e)
        try:
            print('==FIVE SECOND PAUSE TO EXIT USING CTRL-C==')
            time.sleep(5)
        except KeyboardInterrupt:
            break
