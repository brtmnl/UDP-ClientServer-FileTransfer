# -*- coding: utf-8 -*-
"""
@author: emanuele.bertolero@studio.unibo.it
matricola: 0001006540
"""

import socket as sk
import os
from common import *

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

print('\n\rConnecting to server...')
print(HELP_MESSAGE)

while True:
    print('Write a command:')
    command = input()

    if command == 'HELP':
        sent = sock.sendto(command.encode(), server_address)
        data, server = sock.recvfrom(BUFFER_SIZE) 
        print(data.decode('utf8'))

    elif command == 'LIST':
        sent = sock.sendto(command.encode(), server_address)
        data, server = sock.recvfrom(BUFFER_SIZE) 
        print(data.decode('utf8'))
    
    elif command.startswith('GET'):
        sent = sock.sendto(command.encode(), server_address)
        data, server = sock.recvfrom(BUFFER_SIZE)
        args = command.split(' ')
        
        if data.startswith('ERROR'.encode()):
            print(data.decode('utf8'))
            
        else:
            with open(DEFAULT_CLIENT_DOWNLOAD+args[1], "wb") as file:
                file.write(data)
                while True:
                    buffer, server = sock.recvfrom(BUFFER_SIZE)
                    if buffer == 'END'.encode():
                        break
                    file.write(buffer)
            file.close()
            print('The file', args[1] ,'has been successfully downloaded')
            
    elif command.startswith('PUT'):
        args = command.split(' ')
        
        if not os.listdir(DEFAULT_CLIENT_UPLOAD).__contains__(args[1]): #File not found
            print('ERROR The indicated file is not present')
            
        else:
            sent = sock.sendto(command.encode(), server_address)
            data, server = sock.recvfrom(BUFFER_SIZE)
            
            if data.startswith('ERROR'.encode()):
                print(data.decode('utf8'))
                
            elif data.startswith('READY'.encode()):
                with open(DEFAULT_CLIENT_UPLOAD+args[1], "rb") as file:
                    while True:
                        buffer = file.read(BUFFER_SIZE)
                        if not buffer:
                            sent = sock.sendto('END'.encode(), server_address)
                            file.close()
                            break
                        else:
                            sent = sock.sendto(buffer, server_address)
                print('The file', args[1] ,'has been successfully uploaded')
        
        