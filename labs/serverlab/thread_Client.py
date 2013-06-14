#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
from socket import *
import os
import sys
import struct

def Utf(name):
  return name.encode('utf-8')

HOST = '172.18.113.145'
PORT = 10338
ADDR = (HOST, PORT)
BUFSIZE = 10240


tcpSock = socket(AF_INET,SOCK_STREAM)
tcpSock.connect(ADDR)
print tcpSock.recv(BUFSIZE)

while True:
  text = raw_input('>>>')
  if text == 'end': 
    tcpSock.close()
    break
  elif text == 'test':
    tcpSock.send(text)
    print tcpSock.recv(10240)
    fileinfo_size = struct.calcsize(Utf( '256s32sI8s' ))
    fhead = tcpSock.recv(fileinfo_size)
    filename, temp1, filesize, temp2 = struct.unpack(Utf( '256s32sI8s' ), fhead)
    filename = filename.decode('utf-8')
    filename = filename.strip('\x00')
    #filename = os.path.join(os.path.split(filename)[0], 'new_' + os.path.split(filename)[1])
    filename = 'new' + filename

    fp = open(filename, 'wb')
    restsize = filesize

    while True:
      if restsize > BUFSIZE:
        try:
          filedata = tcpSock.recv(BUFSIZE)
        except Exception, e:
          if e.errno == 10054:
            tcpSock.close()
            sys.exit(1)
          else: break
      else:
        filedata = tcpSock.recv(restsize)
      if not filedata: break
      fp.write(filedata)
      restsize = restsize - len(filedata)
      if restsize <= 0: break
    fp.close()
    continue

  print '\tsend: ', text
  tcpSock.send(text)
  ans = tcpSock.recv(10240)
  if not ans: continue
  print '\trecv: ', ans


