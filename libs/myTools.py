#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import sys
import random
import json
import logging as log
import logging.handlers as handlers



def IntStr( num, dec=None ):
  """
  return a str(int), in dec character
  """
  num = int(num)
  if not dec: return str(num)
  if dec <= len(str(num)):
    return str(num)
  ans = "0" * (dec - (len(str(num)))) + str(num)
  return ans

def PathSwitch( path ):
  if not isinstance( path, unicode ):
    try: path = path.decode( 'gbk' )
    except: pass
    try: path = path.decode( 'utf-8' )
    except: pass
  if sys.platform == 'win32':
    return path.encode( 'gbk' )
  else: return path.encode( 'utf-8' )

def RandomChar( length ):
  alphabet = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'

  ans = ''
  for i in range(1, length):
    ans += random.choice(alphabet)

  return ans

def Utf( var ):
  try: var = var.decode('gbk')
  except: pass
  
  try: var = var.decode('utf-8')
  except: pass

  return var.encode('utf-8')



class MyException( Exception ):
  def __init__( self, num, text='none' ):
    Exception.__init__( self )
    self.num = num
    self.text = text

  def __repr__( self ):
    ans = repr(self.num) + ': ' + self.text
    return ans

  def __str__( self ):
    ans = repr(self.num) + ': ' + self.text
    return ans

  def __int__( self ):
    try: return int(self.num)
    except: return 0

class logging():
  def __init__( self, path, log_name, log=log, handlers=handlers ):
    """
    create 3 log file: 
      $log_name + .debug.txt
      $log_name + .info.txt
      $log_name + .error.txt
    """
    if not os.path.exists(path):
      raise MyException( 001, 'logging path: %s' % path )

    logger = log.getLogger(log_name)
    logger.setLevel(log.DEBUG)
    
    debug_logger = log.getLogger('debug')
    debug_logger.setLevel(log.DEBUG)
  
    log_formatter = log.Formatter( 
        '%(name)s - %(asctime)s - %(levelname)s - %(message)s'
        )
    debug_formatter = log.Formatter('%(asctime)s\n%(message)s')
  
    info_handler = handlers.RotatingFileHandler(
        os.path.join(path, log_name) + '.info.txt', \
        mode='a', \
        maxBytes=2097152, \
        backupCount=2
        )
    info_handler.setLevel(log.INFO)
    info_handler.setFormatter(log_formatter)
  
    error_handler = handlers.RotatingFileHandler(
        os.path.join(path, log_name) + '.error.txt', \
        mode='a', \
        maxBytes=5242880, \
        backupCount=1
        )
    error_handler.setLevel(log.ERROR)
    error_handler.setFormatter(log_formatter)
  
    
    debug_handler = handlers.RotatingFileHandler(
        os.path.join(path, log_name) + '.debug.txt', \
        mode='a', \
        maxBytes=5242880, \
        backupCount=2
        )
    debug_handler.setLevel(log.DEBUG)
    debug_handler.setFormatter(debug_formatter)
    
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    debug_logger.addHandler(debug_handler)
  
    self.info_logger = logger
    self.debug_logger = debug_logger

  def debug( self, text ):
    text = json.dumps(text, sort_keys=True, indent=2)
    self.debug_logger.debug(text)

  def info( self, text ):
    self.info_logger.info(text)
  
  def error( self, text ):
    self.info_logger.error(text)


