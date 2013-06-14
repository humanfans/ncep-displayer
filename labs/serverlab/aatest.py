#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import sys

class aaException(Exception):
  def __init__(self, number):
    BaseException.__init__(self)
    self.num = number

  def __repr__(self):
    return repr(self.num)

  def __str__(self):
    return repr(self.num)

  def __int__(self):
    return int(self.num)

def go():
  a = aaException(14)
  raise a

