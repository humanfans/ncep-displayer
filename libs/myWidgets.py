#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import sys
import time
import datetime
import webbrowser
from Tkinter import *
from functools import partial



class myMenu:
  def __init__(self, master):
    print "\ttry to Instance myMenu"
    if (repr(master)[: 20] != '<Tkinter.Tk instance'
        and repr(master)[: 23] != "<Tkinter.Frame instance"):
      print 'master not the Tkinter.Tk instance'
      raise 'myTollbar.__init__:parameterError:'
    print "\tmymenu.__init__'s parameter load ok"
    
    self.master = master
    self.Pwd = sys.path[0]
    #self.Pwd = r'G:\dropbox\Dropbox\Backup\codeSource\qxt\201208_02_display-the-product-of-shuzhiyubao\factor'

  def Draw(self, texts, funcs):
    print "myMenu be called"

    self.funcs = funcs

    master = self.master

    menu = Menu(master)
    master.config(menu=menu)
    exit = partial(os._exit, 1)

    filemenu = Menu(menu)
    menu.add_cascade(label=u'\u83dc\u5355', menu=filemenu) 
    filemenu.add_command(label=u'\u8def\u5f84\u8bbe\u7f6e', \
                         command=funcs['pathChange'])
    #filemenu.add_separator()
    #filemenu.add_command(label=u'\u9000\u51fa', command=exit)

    canvasmenu = Menu(menu)
    menu.add_cascade(label=u'\u5f62\u52bf\u573a', menu=canvasmenu)
    layers = [int(i[1: ]) for i in texts["layerTexts"].keys()]
    layers.sort()
    for eachlayer in layers:
      eachlayer = "C" + str(eachlayer)
      command = partial(funcs["labelFunc"], eachlayer)
      canvasmenu.add_command(label=texts["layerTexts"][eachlayer], \
                             command=command)

    regionmenu = Menu(menu)
    menu.add_cascade(label=u'\u5355\u7ad9\u6a21\u5f0f', menu = regionmenu)
    layers = texts["regionName_order"]
    for eachlayer in layers:
      command = partial(funcs["drawRegion"], eachlayer)
      regionmenu.add_command(label=texts["regionName"][eachlayer], \
                             command=command)

    rainmenu = Menu(menu)
    menu.add_cascade(label=u'\u964d\u6c34\u9884\u62a5', menu=rainmenu)
    layers = texts['RainCateName'].keys()
    layers.sort()
    for eachlayer in layers:
      command = partial(funcs['DrawRain'], layer=eachlayer)
      rainmenu.add_command(label=texts['RainCateName'][eachlayer], \
                           command=command)

    helpmenu = Menu(menu)
    menu.add_cascade(label=u'\u5e2e\u52a9', menu=helpmenu)
    helpmenu.add_command(label="About...", command=self.AboutMe)

  def AboutMe(self):
    funcs = self.funcs
    version = funcs["About"]()["version"]
    mail = funcs["About"]()['mail']
    author = funcs["About"]()['author']
    top = Toplevel()
    top.config(width=300, height=140)
    canvas = Button(top)
    top.title(u'\u5173\u4e8e\u6211')
    canvas.config(bg="#363636", bd=3)
    text = u'Verison\uff1a %s\n' \
           u'\u6d4b\u8bd5\u7248 %s\n' \
           u'\u4f5c\u8005: %s\n' \
           u'\u6709\u4efb\u4f55\u95ee\u9898\u6216\u610f\u89c1\u8bf7\u8054' \
               u'\u7cfb\u6211\n' \
           u'mail: %s\n' \
           u'\u70b9\u51fb\u6253\u5f00\u9879\u76ee\u4e3b\u9875\n\uff08\u68c0' \
           u'\u67e5\u66f4\u65b0\u53ca\u67e5\u770b\u4f7f\u7528\u8bf4\u660e\uff09' \
           % (version, version, author, mail)
    font = ("TimesNewRoman", 10, "normal")
    canvas.config(text=text, anchor=NW, fg="white", font=font, \
                  command=self.OpenHostPage)
    canvas.pack()

  def OpenHostPage(self):
    _Url = 'http://code.google.com/p/nwpdisplayer/'
    webbrowser.open_new_tab(_Url)

  def clipBoard(self):
    string = 'ppcelery@qq.com'
    master = self.master
    master.clipboard_clear()
    master.clipboard_append(string)
     
  def callback(self):
    """
    the default callback
    """
    print "Null >> you did not define the call back"

class myTollbar:
  def __init__(self, master, funcs={}):
    print "\ttry to Instance myTollbar"
    if (repr(master)[: 20] != '<Tkinter.Tk instance'
        and repr(master)[: 23] != "<Tkinter.Frame instance"):
      print 'master not the Tkinter.Tk instance'
      raise 'myTollbar.__init__:parameterError:'   
    if funcs:
      if type(funcs) != dict:
        print 'funcs should be a dict'
        raise 'myTollbar.__init__:parameterError:'
      else:
        for key in funcs.keys():
          if (repr(type(funcs[key])) != "<type 'function'>" 
              and repr(type(funcs[key])) != "<type 'instancemethod'>"):
            print "the funcs key:%s is %s" % (key, repr(type(funcs[key])))
            print "funcs's obj should be a function handle"
            raise 'myTollbar.__init__:parameterError:'
    print "\tmyTollbar.__init__'s parameter load ok"

    self.master = master
    if funcs: self.funcs = funcs
    else: self.funcs = None
    
    print "myTollbar is initialled OK!"

  def Draw(self, side=TOP):
    """
    Draw the toolbar below the menu
    """
    print "myTollbar.Draw be called"
    master = self.master
    toolbar = Frame(master)
    toolbar.pack(side=side, fill=X)

    funcs = self.funcs
    exit = partial(os._exit, 1)
    self.date_text = StringVar()
    date_width = master.winfo_width()
    print date_width

    b_pageup = Button(toolbar, text="<<", width=5, command=funcs["PageUp"])
    b_pagedown = Button(toolbar, text=">>", width=5, command=funcs["PageDown"])
    b_drawtext = Label(toolbar, textvariable=self.date_text, \
                       font=("TimesNewRoman", 11, "bold"), justify=CENTER, \
                       fg="red")
    b_quit = Button(toolbar, text=u'\u9000\u51fa', command=exit)
    b_switchtime = Button(toolbar, text="08/20", width=5, command=funcs["SwitchTime"])
     
    b_switchtime.pack(side=LEFT) 
    b_pageup.pack(side=LEFT)
    b_pagedown.pack(side=LEFT)
    b_drawtext.pack(side=LEFT, expand=True)
    #b_quit.pack(side=RIGHT)

    b_test = Button(toolbar, text=u'\u7ed8\u5e03\u72b6\u6001', 
                    command=self.funcs["CanvasStatus"])
    b_test.pack(side=LEFT)

  def drawText(self, text):
    self.date_text.set(text)

  def callback(self):
    """
    the default callback
    """
    print "Null >> you did not define the call back"

class myCanvas: 
  def __init__(self, master, status):
    print "\tmyCanvas.__init__ try to load parameter..."
    if (repr(master)[: 20] != '<Tkinter.Tk instance'
        and repr(master)[: 23] != "<Tkinter.Frame instance"):
      print 'master not the Tkinter.Tk instance'
      raise 'myCanvas.__init__:parameterError:'  
    print "\tmyCanvas.__init__'s parameter load ok"

    self.master = master
    self.CanvasStatus = status
    self.CanvasStatus["cavs_imgAlbum"] = {}
    self.updateSize = []
    self.updateLocker = datetime.datetime.now() 
    self.whether_text = None
    
    print 'myCanvas initialled OK!'

  def Draw(self, images={}, texts=None, side=TOP, size=None, full=None, \
           funcs=None):
    """
    Draw the region where to display the object
    --------------
    Input:
      images=[] - list: the images which want to display
      side=TOP
      size=None - 2-tuple: the Canvas' (width, height)
    """
    print "Widgets.myCanvas.Draw be called"
    print '\tmyCanvas.Draw: check the parameter...'
    if size:
      if type(size) != list or len(size) != 2:
        raise("Widgets.myCanvas.Draw:parameterError:"
              "size not a 2-list")
    if images:
      if type(images) != dict:
        print "images should be a list or None"
        print "Now the images is %s" % repr(images)
        raise "Widgets.myCanvas.Draw:parameterError"
      for image in images:
        if repr(images[image])[: 32] != '<PIL.ImageTk.PhotoImage instance':
          print "the instance in images should be",
          print "PIL.ImageTk.PhotoImage instance"
          raise 'Widgets.myCanvas.Draw:parameterError:'
      for eachkey in images.keys():
        if eachkey.lower() not in ['a1', 'b1', 'a2', 'b2', 'full']:
          print "images's key should be in ['a1', 'b1', 'a2', 'b2', 'full']"
          raise 'Widgets.myCanvas.Draw:parameterError:'

    print "\tmyCanvas.Draw: try to make frame..."
    if funcs: self.funcs = funcs
    self.updateImagesize = self.funcs["updateImagesize"]
    master = self.master
    if texts:
      self.funcs["drawText"](texts)
    if not size: 
      size = [master.winfo_width()-7, master.winfo_height()-28]
    self.win_size = size
    if images: self.CanvasStatus['Draw_options']['images'] = images
    self.CanvasStatus['Draw_options'].update({"side": side, "size": size, "full": full, \
                              'texts': texts})
    self.whether_full = full
    self.CanvasStatus["whether_full"] = self.whether_full

    if "frame1" in dir(self): self.frame1.pack_forget()
    if "frame2" in dir(self): self.frame2.pack_forget()
    if "frame_full" in dir(self): self.frame_full.pack_forget()
    self.CanvasStatus["cavs_imgAlbum"] = {}

    if not full:
      frame_size = [size[0], (size[1]-50) / 2]
      frames = {'1': '', '2': ''}
      for each_frame in frames:
        frames[each_frame] = self.makeFrame(master=master, size=frame_size)
      self.frame1 = frames['1']
      self.frame2 = frames['2']
  
      print "\tMyCanvas.Draw: try to make canvas..."
      cell_size = [size[0] / 2, size[1] / 2]
      self.cell_size = cell_size
      canvases = {"a1": '', "b1": '', "a2": '', "b2": ''}
      for each_grid in canvases:
        if each_grid[1] == '1':
          the_master = frames[each_grid[1]]
          the_image = None
          the_text = None
          if each_grid in images: the_image = images[each_grid]
          if each_grid in texts: the_text = texts[each_grid]
          canvases[each_grid] = self.makeCanvas(
              master=the_master, size=cell_size, img=the_image, text=the_text
              )
        elif each_grid[1] == '2':
          the_master = frames[each_grid[1]]
          the_image = None
          the_text = None
          if each_grid in images: the_image = images[each_grid]
          if each_grid in texts: the_text = texts[each_grid]
          canvases[each_grid] = self.makeCanvas(
              master=the_master, size=cell_size, img=the_image, text=the_text
              )
      self.CanvasStatus.update({'canvases': canvases})
    elif full:
      if "full" in images and images["full"]: pic = images["full"]
      else:
        for img in images:
          if images[img]:
            pic = images[img]
            break
      text = None
      if "full" in texts:
        if texts["full"]: text = texts["full"]
      self.fullCanvas(img=pic, text=text)

  def displayTexts(self):
    self.whether_text = not self.whether_text
    self.Draw(images=self.CanvasStatus['Draw_options']["images"],
              side=self.CanvasStatus['Draw_options']["side"],
              texts=self.CanvasStatus['Draw_options']["texts"],
              size=self.CanvasStatus['Draw_options']["size"],
              full=self.CanvasStatus['Draw_options']["full"])
 
  def makeFrame(self, master, size=None, bg='#363636', side=TOP, full=None):
    print "myCanvas.makeFrame be called"
    if not full:
      frame = Frame(master)
      frame.config(width=size[0], bg=bg, height=size[1])
      frame.bind("<Configure>", self.updateFrame)
      frame.pack(side=side, fill=BOTH)
    else:
      if not size:
        size = [master.winfo_width()-4, master.winfo_height()-25]
      self.win_size = size
      if "frame1" in dir(self): 
        self.frame1.pack_forget()
        print "\tframe1 be killed"
      if "frame2" in dir(self):
        self.frame2.pack_forget()
        print "\tframe2 be killed"
      frame = Frame(master)
      frame.config(width=size[0], height=size[1], bg=bg, bd=0)
      frame.bind("<Configure>", self.updateFrame)
      frame.pack(side=side, fill=BOTH)
    return frame

  def makeCanvas(self, master, size, side=LEFT, img=None, full=False,
                 bg="#363636", text=None, font=("TimesNewRoman", 13, "bold")):
    """
    make a Canvas Widget
    ---------------
    Input:
      master - toplevel window instance: master
      size - 2-list: [width, height] of the new widget
      side=LEFT - Tkinter.LEFT
      img=None - ImageTk instance: the image to display in this canvas
      full=False - flag: whether to full of the master
      bg="#363636"
      text="None"
      font="("TimesNewRoman", 10, "bold")"
    """
    print "myCanvas.makeCanvas be called"
    print "\tmyCanvas.makeCanvas: check the parameter..."
    if img:
      if repr(img)[: 32] != "<PIL.ImageTk.PhotoImage instance":
        print "Img not the ImageTk instance"
        raise "Widgets.myCanvas.makeCanvas:parameterError"
    if full and not img:
      print "Full Canvas should need at least one img"
      raise "Widgets.myCanvas.makeCanvas:parameterError"
    if (repr(master)[: 20] != "<Tkinter.Tk instance" 
        and repr(master)[: 23] != "<Tkinter.Frame instance"):
      print "master not the Tkinter.Tk or Frame instance"
      print "now the master is", repr(master)
      raise "Widgets.myCanvas.makeCanvas:parameterError:"
    if not full and not size:
      print "you should input a size like 2-list"
      raise "Widgets.myCanvas.makeCanvas:parameterError:"
    print "\tparameter is ok"
    canvas = Canvas(master)
    if img:
      new_img = self.updateImagesize(pic=img, size=size)
      for key in self.CanvasStatus['Draw_options']["images"]:
        if self.CanvasStatus['Draw_options']["images"][key] == img:
          self.CanvasStatus['Draw_options']["images"][key] = new_img
      img = new_img
      x_blank = (size[0] - new_img.width()) / 2
      y_blank = (size[1] - new_img.height()) / 2
      canvas.create_image(x_blank, y_blank, image=img, anchor=NW)
      self.CanvasStatus["cavs_imgAlbum"].update({str(canvas): img})
      print "\timg:%s be loaded" % str(canvas)
    else:
      x_blank = int(size[0] / 2)
      y_blank = int(size[1] / 2)
      text_id = canvas.create_text(x_blank, y_blank, text=u'\u7f3a\u7701',
                                   font=("TimesNewRoman", 20, "bold"),
                                   anchor=CENTER, fill="white")
    if text and self.whether_text:
      x_blank = 5
      y_blank = 0
      if full: y_blank = 5
      font=("TimesNewRoman", 13, "bold")
      canvas.create_text(x_blank, y_blank, fill="red",
                         text=text, font=font, anchor=NW)
      try:
        print "\ttext:%s be loaded" % text
      except:
        pass
    canvas.bind('<Button-3>', self.funcs['Image2Clipboard'])
    if not full:
      canvas.config(width=size[0], height=size[1], bg=bg)
      if img:
        canvas.bind("<Double-Button-1>", self.fullCanvas)
    else:
      canvas.config(width=size[0], height=size[1], bd=0)
      self.thefullCanvas = canvas
      canvas.bind("<Double-Button-1>", self.cellCanvas)
    canvas.pack(side=side, fill=BOTH)
    print '\tcanvas:', canvas, 'pack ok!'
    return canvas

  def fullCanvas(self, event=None, img=None, text=None):
    print "myCanvas.fullCanvas be called"
    self.whether_full = True
    self.CanvasStatus["whether_full"] = self.whether_full
    master = self.master 
    if not img:
      pointer = [event.x_root, event.y_root]
      pic = master.winfo_containing(pointer[0], pointer[1])
      for the_grid in self.CanvasStatus['canvases']:
        if self.CanvasStatus['canvases'][the_grid] == pic:
          self.CanvasStatus['grid'] = the_grid
          break
      img = self.CanvasStatus['cavs_imgAlbum'][str(pic)]
      self.CanvasStatus["cavs_imgAlbum"] = {str(pic): img}
    else: self.CanvasStatus['cavs_imgAlbum'] = {}
    self.CanvasStatus['Draw_options']["images"]["full"] = img
    frame_full = self.makeFrame(master=master, full=True)
    self.frame_full = frame_full
    size = self.win_size
    if self.whether_text and 'full' in self.CanvasStatus['Draw_options']["texts"]:
      text = self.CanvasStatus['Draw_options']['texts']['full']
    else: text = ''
    if self.CanvasStatus['mode'] == 'REGION' \
        and self.CanvasStatus['grid'] == 'a2':
      self.CanvasStatus.update({'layer': 'C18'})
    self.makeCanvas(master=frame_full, size=size, img=img, full=True, text=text)

  def cellCanvas(self, event):
    print "myCanvas.cellCanvas be called"
    name = repr(self.frame_full)
    self.frame_full.pack_forget()
    print name, 'is destroyed'
    self.whether_full = False
    self.CanvasStatus["whether_full"] = self.whether_full
    if self.CanvasStatus['mode'] == 'REGION' \
        and self.CanvasStatus['layer'] == 'C18':
      self.CanvasStatus.update({'layer': 'C17'})
    self.Draw(images=self.CanvasStatus['Draw_options']["images"], \
              side=self.CanvasStatus['Draw_options']["side"], \
              texts=self.CanvasStatus['Draw_options']["texts"], \
              size = self.CanvasStatus['Draw_options']['size'])

  def updateFrame(self, event):
    master = self.master
    if self.whether_full:
      size = [master.winfo_width()-4, master.winfo_height()-25]
    else: size = [master.winfo_width()-7, master.winfo_height()-28]
    if size == self.updateSize: return ""
    the_time = datetime.datetime.now() - self.updateLocker
    if the_time.microseconds % 1000000 < 100000 and the_time.seconds < 1:
      return ""
    print "myWidgets,updateFrame be called"
    self.updateSize = size
    self.updateLocker = datetime.datetime.now()
    full = self.whether_full
    self.Draw(full=full, size=size,
              images=self.CanvasStatus['Draw_options']["images"],
              side=self.CanvasStatus['Draw_options']["side"],
              texts=self.CanvasStatus['Draw_options']["texts"])
