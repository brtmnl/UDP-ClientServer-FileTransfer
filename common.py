# -*- coding: utf-8 -*-
"""
@author: emanuele.bertolero@studio.unibo.it
matricola: 0001006540
"""
import os

server_address = ('localhost', 10000)
BUFFER_SIZE = 4096
DEFAULT_CLIENT_DOWNLOAD=os.getcwd()+"/client/download/"
DEFAULT_CLIENT_UPLOAD=os.getcwd()+"/client/upload/"
DEFAULT_SERVER_PATH = os.getcwd()+"/server/archive/"
HELP_MESSAGE = 'Use one of the following commands: \n\r\n\r - LIST: to get the list of files that are stored \n\r - GET "filemane": to download the indicated file \n\r - PUT "filemane" to upload the indicated file \n\r - HELP: to get help via this same message'
