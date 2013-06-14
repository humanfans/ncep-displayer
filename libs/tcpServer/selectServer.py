#! /usr/bin/env python
# -*- coding: utf-8



from __future__ import unicode_literals
import os
import sys
import socket
import select
import datetime
import makegs
from myTools import logging
from myTools import PathSwitch
from myTools import MyException
from myTools import RandomChar
from myTools import Utf
                               


class ServerError( MyException ):
  def __init__( self, num, text ): 
    MyException.__init__( self, num, text )



class SelectServer:
                                                                                      
  def __init__( self, port=10338, bufsize=10340 ):
    """
    create a host server
    """
    self.args = {
        'hostPort': port, \
        'bufSize': bufsize, \
        'sockDict': {}, \
        'clientDict': {}, \
        'threadDict': {}, \
        'tokenDict': {}, \
        }

    self.logger = logging( os.path.abspath(os.curdir), 'SelectServer' )

    self.args['hostSock'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.args['hostsock'].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.args['hostSock'].bind(("", port))
    self.args['hostSock'].listen(5)

    self.args['sockDict'].update({hostSock: ''})
    self.logger.debug( self.args )

    def Run( self ):
      """
      start the server
      """

      while True:
        (sread, swrite, sexc) = select.select(
            self.args['sockDict'].keys(), [], [], 0
            )

        for sock in sread:
          if sock == self.args['hostSock']:
            new_sock, (remhost, remport) = self.args['hostSock'].accept()
            new_sock.settimeout(15)
            host, port = new_sock.getpeername()
            self.logger.info(
                'accept new connection from\t%s:%s\t' % (host, port)
                )
            try:
              self.NewConnection( new_sock )
            except: continue
          else: continue

    def Collector( self, sock ):
      """
      delete a ClientInServer instance and collect the rem
      """
      #TODO
 
    def CreateClient( self, sock ):
      #TODO create a client instance

    def NewConnection( self, sock ):
      """
      accept a new connection from a client
        check its id and password, 
        create a identify toke
        assign disk room and create a .gs file
        create a ClientInServer instance
      """
      count = 0
      addr, port = sock.getpeername()

      while count < 10:
        try: 
          data = sock.recv( 10340 )
        except Exception, e:
          self.logger.error( 'create a NewConnection error: %s' % repr(e))
          count += 1
          continue

        if not data: 
          count += 1
          continue

        token, temp1, the_type, temp2, content = \
            struct.unpack(Utf( '32s2s64s2s10240s' ), data)
        if the_type.strip('\x00').decode('utf-8') != 'verify':
          count += 1
          continue

        # default ID and password is qxt@dqyb188
        content = content.decode('utf-8').strip('\x00')
        user_name, passwd = content.split('@')
        if user_name != 'qxt' or passwd != 'dqyb188':
          self.logger.info( 
              'verify error! user_name: %s, passwd: %s' % (user_name, passwd)
              )
          sock.close()
          return None
        else:
          self.logger.info(
              'user: %s is log in' % user_name)
          
          while True:
            new_token = RandomChar( 32 )
            if new_token in self.args['tokenDict'].keys(): continue

          verify_back = struck.pack(
              Utf( '32s2s64s2s10240s' ), \
              Utf( new_token ), Utf( ?? ), Utf( 'new_token' ), \
              Utf( '??' ), Utf( new_token )
              )

        send_count = 0
        while send_count <= 3:
          try:
            sock.send(verify_back)
            break
          except Exception, e:
            send_count += 1
            self.logger.error( 'send verify_back message error: %s' % e )
            continue

        if send_count > 3: break

        dirs = os.path.abspath(os.curdir)
       
        new_doc = os.path.join(dirs, new_token)
        new_doc = PathSwitch( new_doc )
        try:
          os.makedirs(new_doc)
        except Exception, e:
          sock.close()
          self.logger.error( 'failed to create a new doc: %s' % new_doc)
          raise ServerError( 001, 'failed to create a new doc: %s' % new_doc )

        try: #TODO
          new_gs = makegs.Make(
              gsFilePath=r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\test.gs', \
              dataFilePath=r'X:\pressure\air.1998.nc', \
              resultPath=r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\res', \
              gradsExecPath = r'X:\GrADS19\win32\grads.exe'
              )
        except Exception, e:
          sock.close()
          self.logger.error( 'failed to create a makegs instance' )
          raise ServerError( 002, 'failed to create a makegs instance' )
        
        #TODO create a ClientInServer instance

        self.args['sockDict'].update({sock: ''})
        self.args['tokenDict'].update({new_token: ''})
        self.logger.debug( self.args )

      self.logger.info( 
          "do not accept valid message, close the sock form %s:%s" \
          % (addr, port)
          )
      sock.close()
      return None
