#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
from socket import *
import os
import struct

def Utf(name):
  return name.encode('utf-8')

HOST = '172.18.113.145'
PORT = 10338
ADDR = (HOST, PORT)
BUFSIZE = 1024
filename = r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\test\_Combine.jpeg'
FILEINFO_SIZE=struct.calcsize(Utf('128s32sI8s'))

tcpSock = socket(AF_INET,SOCK_STREAM)
tcpSock.connect(ADDR)

fhead=struct.pack(Utf('128s11I'), Utf(filename), 0,0,0,0,0,0,0,0, os.stat(filename).st_size, 0,0)
tcpSock.send(fhead)

fp = open(filename, 'rb')
while 1:
    filedata = fp.read(BUFSIZE)
    if not filedata: break
    tcpSock.send(filedata)
fp.close()

tcpSock.close()
