#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import sys
import random
import json
import codecs
import logging as log
import logging.handlers as handlers


# Author: Laisky
# Version: 1.1
# Date: 2013-06-18


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


def LoadConfig( file_path, multi_arg=False, coding="GBK", split="\t", comment="#" ):
  config_data = codecs.open(file_path, "r", coding).readlines()

  result = {}
  for each_config in config_data:
    each_config = each_config.strip()
    if comment in each_config: each_config = each_config[: each_config.index(comment)]
    if not each_config: continue
    arg_key, arg_cont = [i for i in each_config.split(split) if i]

    if not multi_arg:
      result.update({arg_key: arg_cont})
    elif multi_arg:
      if arg_key not in result:
        result.update({arg_key: [arg_cont]})
      elif not isinstance(result[arg_key], list):
        result[arg_key] = [result[arg_key], arg_cont]
      else:
        result[arg_key].append(arg_cont)

  return result


def MemManager( doc_path, max_mem=2.0 ):
  """
  manage the doc's memory
  remove the oldest files
  if max_men = 0
  ----------
    doc_path - str: the doc's path
    max_mem - int: mBytes
  """
  if max_mem == 0: return None

  the_files = os.walk(doc_path).next()[2]
  file_dic = {}
  for each_file in the_files:
    file_path = os.path.join(doc_path, each_file)
    file_date = os.stat(file_path).st_ctime
    file_dic.update({file_date: file_path})

  time_sort = file_dic.keys()
  time_sort.sort(reverse=True)

  file_size = 0
  for each_time in time_sort:
    file_path = file_dic[each_time]
    file_size += os.stat(file_path).st_size / 1024. / 1024.
    if file_size > max_mem:
      try:
        file_path = PathSwitch( file_path )
        os.remove(file_path)
      except: pass



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
  def __init__(
      self, path, log_name, log=log, handlers=handlers,
      disabled=False
      ):
    """
    create 3 log file:
      $log_name + .debug.txt
      $log_name + .info.txt
      $log_name + .error.txt
    """
    self.disabled = disabled
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
        backupCount=1
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
    if self.disabled: return None

    text = json.dumps(text, sort_keys=True, indent=2)
    self.debug_logger.debug(text)

  def info( self, text ):
    if self.disabled: return None

    self.info_logger.info(text)

  def error( self, text ):
    if self.disabled: return None

    self.info_logger.error(text)



