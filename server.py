# -*- coding: utf-8 -*-
"""
@author: emanuele.bertolero@studio.unibo.it
matricola: 0001006540
"""

import socket as sk
import os
from common import *

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
server_address = ('localhost', 10000)
print ('\n\r starting up on %s port %s' % server_address)
sock.bind(server_address)


while True:
    
    try:
        print('\n\r waiting to receive message...')
        data, address = sock.recvfrom(BUFFER_SIZE)
        print (data.decode('utf8'))
        
        if data.decode('utf8') == 'LIST': #Comando LIST
            l = os.listdir(DEFAULT_SERVER_PATH)
            sent = sock.sendto(str(l).encode(), address)
            print ('Answered the LIST command, sent to %s %s bytes' % (address, sent))
        
        if data.decode('utf8') == 'HELP': #Comando HELP
           sent = sock.sendto(HELP_MESSAGE.encode(), address)
           print ('Answered the HELP command, sent to %s %s bytes' % (address, sent))
            
        if data.decode('utf8').startswith('GET'): #Comando GET
            args = data.decode('utf8').split(' ')
            
            if len(args) == 1: #Missed file name
                data = 'ERROR Expected a file name as an argument'
                sent = sock.sendto(data.encode(), address)
                print ('Answered the GET command, sent to %s %s bytes' % (address, sent))
                
            elif not os.listdir(DEFAULT_SERVER_PATH).__contains__(args[1]): #File not found
                data = 'ERROR The indicated file is not present'
                sent = sock.sendto(data.encode(), address)
                print ('Answered the GET command, sent to %s %s bytes' % (address, sent))
                
            else:
                try:
                    with open(DEFAULT_SERVER_PATH+args[1], 'rb') as file:
                        while True:
                            buffer = file.read(BUFFER_SIZE)
                            if not buffer:
                                sent = sock.sendto('END'.encode(), address)
                                file.close()
                                break
                            else:
                                sent = sock.sendto(buffer, address)
                
                except IOError:
                    data = 'ERROR Generic error to donwload the file'
                    sent = sock.sendto(data.encode(), address)
                    print ('Answered the GET command, sent to %s %s bytes' % (address, sent))
                    continue
        
        if data.decode('utf8').startswith('PUT'): #Comando PUT
            args = data.decode('utf8').split(' ')
            
            if len(args) == 1: #Missed file name
                data = 'ERROR Expected a file name as an argument'
                sent = sock.sendto(data.encode(), address)
                print ('Answered the PUT command, sent to %s %s bytes' % (address, sent))
                
            elif os.listdir(DEFAULT_SERVER_PATH).__contains__(args[1]): #File already present
                data = 'ERROR The indicated file is already present'
                sent = sock.sendto(data.encode(), address)
                print ('Answered the PUT command, sent to %s %s bytes' % (address, sent))
                
            else:
                try:
                    rec = sock.sendto('READY'.encode(), address)
                    with open(DEFAULT_SERVER_PATH+args[1], 'wb') as file:
                        while True:
                            buffer, server = sock.recvfrom(BUFFER_SIZE)
                            if buffer == 'END'.encode():
                                file.close()
                                break
                            else:
                                file.write(buffer)
                
                except IOError:
                    data = 'ERROR Generic error to upload the file'
                    sent = sock.sendto(data.encode(), address)
                    print ('Answered the PUT command, sent to %s %s bytes' % (address, sent))
                    continue
        
    except Exception as info:
        print(info)
