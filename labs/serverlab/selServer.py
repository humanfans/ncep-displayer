#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import socket
import select
import struct
                                                                                      
#debug = False
debug = True


def Utf( name ):
  return name.encode('utf-8')

                                                                                      
class ChatServer:
                                                                                      
  def __init__( self, port ):
    if debug: print 'start init ChatServer'
    self.port = port
    self.srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    self.srvsock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    self.srvsock.bind( ("", port) )
    self.srvsock.listen( 5 )
                                                                                      
    self.descriptors = [self.srvsock]
    print 'ChatServer started on port %s' % port
                                                                                      
  def run( self ):
                                                                                          
    while 1:
      # Await an event on a readable socket descriptor
      (sread, swrite, sexc) = select.select( self.descriptors, [], [], 0 )
                                                                                           
      # Iterate through the tagged read descriptors
      for sock in sread:
        # Received a connect to the server (listening) socket
        if sock == self.srvsock:
          self.accept_new_connection()
        else:
          # Received something on a client socket
          try:
            str = sock.recv( 10240 )
          except:
            sock.close()
            self.descriptors.remove( sock )
            break
          # Check to see if the peer socket closed
          if str == '':
            host,port = sock.getpeername()
            str = 'Client left %s:%s/r/n' % (host, port)
            self.broadcast_string( str, sock )
            sock.close
            self.descriptors.remove( sock )
          elif str == 'test':
            fileinfo_size = struct.calcsize( '256s32sI8s'.encode('utf-8') )
            filename = r'_Combine.jpeg'
            fhead = struct.pack( Utf( '256s11I' ), Utf( filename ), 0,0,0,0,0,0,0,0, os.stat(filename).st_size, 0,0 )
            print fhead
            sock.send( fhead )

            fp = open(filename, 'rb')

            while True:
              filedata = fp.read(10240)
              if not filedata: break
              try:
                sock.send(filedata)
              except Exception, e:
                if e.errno == 10054:
                  sock.close()
                  self.descriptors.remove(sock)
                break
            
            fp.close

          else:
            host,port = sock.getpeername()
            newstr = '[%s:%s] %s' % (host, port, str)
            self.broadcast_string( newstr, sock )
                                                                                      
  def accept_new_connection( self ):
    if debug: print 'accept new connection...'
    newsock, (remhost, remport) = self.srvsock.accept()
    self.descriptors.append( newsock )
    newsock.send( "You're connected to the Python chatserver/r/n" )
    str = 'Client joined %s:%s/r/n' % (remhost, remport)
    self.broadcast_string( str, newsock )
                                                                                      
  def broadcast_string( self, str, omit_sock ):
    if omit_sock == self.srvsock: return None
    omit_sock.send(str)
                                                                                      
myServer = ChatServer( 10338 ).run()

