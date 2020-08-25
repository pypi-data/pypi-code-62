# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 15:41:07 2017

@author: devin
"""

import socket
from datetime import datetime
from time import sleep
import time

class socket_control:
    
    def __init__(self, iAddr, iPort = 5025):
        self.ip_addr = iAddr
        self.port = iPort
        
    def __del__(self):
        self.Close()
        
    def Send(self, String):
        ByteString = bytes(String, encoding = 'utf-8')
        self._sock.send(ByteString)
        return self.Receive()
        
    def Receive(self, MaxBytes=2048):
        ByteString = self._sock.recv(MaxBytes)
        String = str(ByteString, encoding = 'utf-8')
        if String.endswith('\n'):
            String = String.rstrip('\n')
        return String
        
    def Connect(self, Mode = 'TCP'):
        if Mode == 'TCP' :
            print('IP = {} and port = {}'.format(self.ip_addr, self.port))
            self._sock = socket.create_connection([self.ip_addr, self.port], timeout = 3)
            self.IDN = self.Send('*idn?')
            print(self.IDN)
        else:
            self._udp = socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._udp.settimeout(3)
        
    def Close(self):
        self._sock.close()
        
        
        
        