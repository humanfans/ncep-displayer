#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
from socket import *
import os
import struct

HOST = '172.18.113.145'
PORT = 10338
ADDR = (HOST, PORT)
BUFSIZE = 1024
FILEINFO_SIZE=struct.calcsize('128s32sI8s'.encode('utf-8'))

recvSock = socket(AF_INET,SOCK_STREAM)
recvSock.bind(ADDR)
recvSock.listen(True)

print "wait..."
conn, addr = recvSock.accept()
print "recv from ", addr

fhead = conn.recv(FILEINFO_SIZE)
filename, temp1, filesize, temp2 = struct.unpack('128s32sI8s'.encode('utf-8'),fhead)

filename = filename.decode('utf-8')
filename = filename.strip('\x00')
filename = os.path.join(os.path.split(filename)[0], 'new_' + os.path.split(filename)[1])
print filename
fp = open(filename,'wb')
restsize = filesize
while 1:
    if restsize > BUFSIZE:
        filedata = conn.recv(BUFSIZE)
    else:
        filedata = conn.recv(restsize)
    if not filedata: break
    fp.write(filedata)
    restsize = restsize-len(filedata)
    if restsize == 0: break
fp.close()

conn.close()
recvSock.close()

raw_input('')
