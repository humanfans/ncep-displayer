#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
from Tkinter import *
import os
import sys




master = Tk()

listbox = Listbox(master)

def shuchu( event ):
  print listbox.get(listbox.curselection())

scroll = Scrollbar(master)
scroll.config(command=listbox.yview)

listbox.config(width=30, height=30)

for item in ['i888888888888888888888888888888888888i' + str(i) for i in range(1, 40)]:
  listbox.insert(END, item)

listbox.config(yscrollcommand=scroll.set)
listbox.bind('<Double-Button-1>', shuchu)

listbox.pack(side=LEFT, expand=True, fill=BOTH)
scroll.pack(side=RIGHT, fill=BOTH)

mainloop()
