#! /usr/bin/env python
# -*- coding: utf-8



from __future__ import unicode_literals
from Tkinter import *
import os
import sys
import types



class dataStream( dict ):

  def __init__( self, data ):
    """
    a datastream manager depend on python's dict
    """
    dict.__init__( data )
    self.data = data

    # initialled the Tkinter *Var
    for cate in data:
      for arg in cate:
        if not isinstance(data[cate][arg], types.ListType): continue
        if not (isinstance(data[cate][arg][1], IntVar)
                or isinstance(data[cate][arg][1], StringVar)): continue
        value = data[cate][arg][0]
        data[cate][arg][1].set(value)

  def synchro( self ):
    """
    synchro the dataStream
    from Tkinter *Var to string/int
    """
    data = self.data
    bool_arg = self._ArgsCheck()

    for cate in data:
      for key in data[cate]:
        if not isinstance(data[cate][key], types.ListType):
          continue
        if not (isinstance(data[cate][key][1], StringVar)
                or isinstance(data[cate][key][1], IntVar)):
          continue
        try:
          data[cate][key][0] = data[cate][key][1].get()
        except: pass

    self.logger.debug( repr(data) )
    if not bool_arg: return None
    return True