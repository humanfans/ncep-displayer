#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
from socket import *
import os
import struct
import time
import threading
import random

HOST = '172.18.113.145'
PORT = 10338
ADDR = (HOST, PORT)
BUFSIZE = 10240
#FILEINFO_SIZE=struct.calcsize('128s32sI8s'.encode('utf-8'))

recvSock = socket(AF_INET,SOCK_STREAM)
recvSock.bind(ADDR)
recvSock.listen(3)

threadLib = {}


def PersonalServer(connect, addr, bufsize=10240):
  while True:
    try:
      data = conn.recv(bufsize)
    except:
      break
    if not data: continue
    print data
    if data.strip() == 'end':
      break
    else:
      conn.send(time.ctime())
  return None

def ThreadIsAlive(thread_dict):
  for key in thread_dict:
    if not thread_dict[key].isAlive():
      del thread_dict[key]

while True:
  print "wait..."
  conn, addr = recvSock.accept()
  print "recv from ", addr
  name = random.random
  threadLib.update({name: threading.Thread(target=PersonalServer, \
                                           args=[conn, addr, 10240])})
  threadLib[name].start()
  ThreadIsAlive(threadLib)


raw_input('')
