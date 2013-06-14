#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import sys
from functools import partial
from Tkinter import *
from myTools import Utf

master = Tk()

def ff( var ):
  print var.get()

class Toollit( Toplevel ):
  def __init__( self, master=None ):
    Toplevel.__init__(self, master=master)
    if master: self.transient(master)

    frame1 = Frame(master=self)
    frame2 = Frame(master=self)

    frame1.pack(fill=BOTH, expand=True)
    frame2.pack(fill=BOTH, expand=True)

    self.label1 = Label(master=frame1, text=Utf( '测试1' ), bg='green')
    self.label2 = Label(master=frame2, text=Utf( '测试2' ), bg='red')
    self.label1.pack(fill=BOTH, expand=True)
    self.label2.pack(fill=BOTH, expand=True)


    self.config(bg='#363636', bd=0)
    self.frame1 = frame1
    self.frame2 = frame2

    self.bind('<Configure>', self.debug)

  def debug( self, event ):
    print 'event x:y\t%s\t%s' % (event.width, event.height)
    print 'frame x:y\t%s\t%s' % (self.frame1.cget('width'), self.frame1.cget('height'))
    print 'label x:y\t%s\t%s' % (self.label1.cget('width'), self.label1.cget('height'))

class myMenu( Menu ):
  def __init__( self, master ):
    Menu.__init__( self, master=master )
    master.config(menu=self)

    filemenu = Menu(self)
    childmenu = Menu(filemenu)
    self.add_cascade(label=Utf( '测试' ), menu=filemenu)
    filemenu.add_command(label=Utf( '测试-测试' ))
    filemenu.add_cascade(label=Utf( '测试2' ), menu=childmenu)
    childmenu.add_command(label=Utf( '测试3' ))

    #self.pack()


x = 0
y = 1
class myButton( Checkbutton ):
  def __init__( self, master, text, geo ):
    Checkbutton.__init__(self, master)

    var = IntVar()
    x, y = geo


    command = partial(ff, var)
    self.config(text=text, variable=var, onvalue=1, offvalue=0, command=command)
    self.grid(row=x, column=y, sticky=W)




modes = [
        ('first', 1),
        ('second', 2),
        ('third', 3)
        ]
buttons = []

#toollit = Toollit( master )
#menu = myMenu( master )
#button = myButton( master, 'first', [1, 1] )
#button = myButton( master, 'sec', [2, 1] )
#button = myButton( master, 'thir', [3, 1] )

vv = StringVar()
vv.set('asd')
#OptionMenu(master, vv, *[1,2,3,4,5] ).pack()


var = StringVar()
var.set('start')

def ff1( var ):
  print var.get()

def ff2( var ):
  var.set('asd')

cc1 = partial(ff1, var)
cc2 = partial(ff2, var)


#Entry(master, textvariable=var).pack()
#Button(master, text='shuchu', command=cc1).pack()
#Button(master, text='change', command=cc2).pack()

Radiobutton(master, text='111', variable=var, value=1, command=cc1).pack()
Radiobutton(master, text='222', variable=var, value=2, command=cc1).pack()




master.mainloop()
