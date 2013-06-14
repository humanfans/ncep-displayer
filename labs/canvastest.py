#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
from Tkinter import *
from PIL import Image, ImageTk
import os
import sys

root = Tk()

pic = ImageTk.PhotoImage( Image.open(r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\libs\1.jpeg') )

cc = Canvas(root)
cc.create_image(10, 10, image=pic, anchor=NW)
cc.config(bg='#363636')
cc.pack(expand=True, fill=BOTH)

mainloop()
