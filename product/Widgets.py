#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
from Tkinter import *
import os
import sys
import types
import pickle
import time
import datetime
import calendar
import win32clipboard
import tkFileDialog
from threading import Thread
from cStringIO import StringIO
from PIL import Image, ImageTk
from functools import partial
from myTools import logging
from myTools import MyException
from myTools import MemManager
from myTools import PathSwitch
from myTools import IntStr



class WidgetError( MyException ):
  def __init__( self, num, text=None ):
    MyException.__init__( self, num, text )


class MainMenu( Menu ):

  def __init__( self, master, dataStream ):
    Menu.__init__( self, master=master )
    master.config(menu=self)

    self.logger = logging(
        dataStream['sysArgs']['hostPath'], __name__ + '.Menu'
        )
    self.logger.info(
        '.__init__(master=%s, dataStream=%s)'
        % (repr(master), repr(dataStream))
        )

    try:
      image_path = os.path.join(
          dataStream['sysArgs']['hostPath'], "icons", "dirs.jpg"
          )
      image_path = PathSwitch( image_path )
      icon_dirs = Image.open(image_path)
      self.icon_dirs = ImageTk.PhotoImage(icon_dirs)
    except IOError:
        self.logger.error( "003: icon_dirs: %s" % repr(image_path) )
        raise WidgetError( 3, "icon_dirs: %s" % repr(image_path) )

    self.dataStream = dataStream
    self.master = master

  def draw( self, texts ):
    """
    make menu by a list
    texts is [('name', func), ('name', [('name', func)])]
    """
    if not isinstance(texts, types.ListType):
      self.logger.error( '001 texts: %s' % repr(texts) )
      raise WidgetError( 001, "Menu.draw's arg texts should be list" )
    self.logger.info( '.draw(texts=%s)' % repr(texts) )

    self._MakeMenu( self, texts )

  def PathConfig( self, event=None ):
    """
    create a new window to configure the path args
    """
    self.logger.info( '.PathConfig()' )

    root = self.master
    data = self.dataStream

    master = Toplevel()

    # set the path_config window's size and title
    screen_size = [root.winfo_screenwidth(), root.winfo_screenheight()]
    size = [420, 180]
    master.minsize(*size)
    master.resizable(False, False)
    master.transient(root)
    master.title('系统参数设定')
    master.geometry(
        "380x180+%s+%s"
        % (int(screen_size[0]*0.5)-210, int(screen_size[1]*0.5)-90)
        )


    # load the dataStream['sysArgs'] from datafile
    try:
      file_path = os.path.join(data['sysArgs'][hostPath], 'arg_data.dat')
      file_path = PathSwitch( file_path )
      with open(file_path, 'rb') as data_file:
        data['sysArgs'].update(pickle.load(data_file))
    except: pass

    # initiall the path_config's frame
    frame_top = Frame(master)
    frame_mid = Frame(master)
    frame_down = Frame(master)

    frame_top.pack(expand=True, fill=BOTH)
    frame_mid.pack(expand=True, fill=BOTH)
    frame_down.pack(expand=True, fill=BOTH)

    # initiall the Tkinter's Var
    grads_exec_path = StringVar()
    ncep_data_path = StringVar()
    img_doc_path = StringVar()
    max_mem_size = DoubleVar()
    hint_info = StringVar()

    grads_exec_path.set(data['sysArgs']['gsExecPath'])
    ncep_data_path.set(data['sysArgs']['gsDataPath'])
    img_doc_path.set(data['sysArgs']['gsDocPath'])
    max_mem_size.set(data['sysArgs']['maxDocSize'])
    hint_info.set('')

    # todo change to grid geometry
    Label(frame_top).grid(column=0, row=1)
    Label(
        frame_top, text='GrADs执行文件路径  (*\\grads.exe)',
        ).grid(row=1, column=0, columnspan=2, sticky=W)
    Entry(
        frame_top, textvariable=grads_exec_path, width=60
        ).grid(row=3, column=1, sticky=W)
    Label(frame_top).grid(row=3, column=2)
    command = partial(
        self.openFileDialog, hint_info, prepath=grads_exec_path,
        initialfile="grads.exe", variable=grads_exec_path
        )
    Button(
        frame_top, text="...", command=command,
        image=self.icon_dirs
        ).grid(row=3, column=3, sticky=E)

    Label(
        frame_top, text='NCEP数据文件路径',
        ).grid(row=5, column=0, columnspan=2, sticky=W)
    Entry(
        frame_top, textvariable=ncep_data_path, width=60
        ).grid(row=7, column=1, sticky=W)
    command = partial(
        self.openFileDialog, hint_info, prepath=ncep_data_path,
        open_dirs=True, variable=ncep_data_path
        )
    Button(
        frame_top, command=command,
        image=self.icon_dirs,
        ).grid(row=7, column=3, sticky=E)

    Label(
        frame_top, text='图片缓存文件夹路径',
        ).grid(row=9, column=0, columnspan=2, sticky=W)
    Entry(
        frame_top, textvariable=img_doc_path, width=60
        ).grid(row=11, column=1, sticky=W)
    command = partial(
        self.openFileDialog, hint_info, prepath=img_doc_path,
        open_dirs=True, variable=img_doc_path
        )
    Button(
        frame_top, text="...", command=command,
        image=self.icon_dirs
        ).grid(row=11, column=3, sticky=E)

    Label(
        frame_mid, text='最大缓存空间  （0为不限制）'
        ).pack(side=LEFT, fill=BOTH)
    Entry(
        frame_mid, textvariable=max_mem_size,
        ).pack(side=LEFT, fill=X)
    Label(frame_mid, text='  MB').pack(side=LEFT, fill=BOTH)

    path_args = {
        'grads_exec_path': grads_exec_path,
        'ncep_data_path': ncep_data_path,
        'img_doc_path': img_doc_path,
        }
    command = partial(
        self._PathCheck, master, path_args, max_mem_size, hint_info
        )
    Label(
        frame_down, textvariable=hint_info, fg="red"
        ).pack(side=LEFT, expand=True, fill=X)
    Button(
        frame_down, text='确认', width=20, command=command
        ).pack(side=RIGHT, fill=BOTH)

  def openFileDialog(
        self, hint_info, variable, prepath=None, event=None,
        initialfile=None, open_dirs=False
        ):
    """
    open file dialog
    """
    self.logger.info(
        ".open(hint_info=%s, prepath=%s, event=%s)"
        % (repr(hint_info), repr(prepath), repr(event))
        )

    prepath = prepath.get()

    if not prepath:
      prepath = self.dataStream['sysArgs']['hostPath']

    if os.path.isfile(prepath):
      prepath = os.path.dirname(prepath)

    if not os.path.isdir(prepath):
      hint_info.set('"%s"不存在' % prepath)

    # todo error
    if not open_dirs:
      file_dialog = tkFileDialog.askopenfilename(
          parent=self.master, defaultextension=".exe",
          filetypes=[("执行文件", ".exe"), ("数据文件", ".nc")],
          initialdir=prepath, initialfile=initialfile
          )
      if not file_dialog: return None
      if "/" in file_dialog:
        file_dialog = '\\'.join(file_dialog.split('/'))
      variable.set(file_dialog)
    elif open_dirs:
      file_dialog = tkFileDialog.askdirectory(
          parent=self.master,
          initialdir=prepath, initialfile=initialfile
          )
      if not file_dialog: return None
      if "/" in file_dialog:
        file_dialog = '\\'.join(file_dialog.split('/'))
      variable.set(file_dialog)

  def _PathCheck(
      self, master, path_args, max_mem_size, hint_info, event=None
      ):
    """
    check whether the path is existed
    """
    self.logger.info(
        '_PathCheck(path_args=%s, hint_info=%s, event=%s)'
        % (repr(path_args), repr(hint_info), repr(event))
        )

    data = self.dataStream
    hint_info.set('')

    # todo wait to add complicted args check

    # path check
    for each_arg in path_args:
      try:
        the_path = path_args[each_arg].get()
      except ValueError:
        hint_info("输入错误")
        return None
      the_path = PathSwitch( the_path )
      if not os.path.exists(the_path):
        hint_info.set('“%s” 不存在' % the_path)
        return None

    # memory check
    try:
      mem_size = max_mem_size.get()
    except ValueError:
      hint_info.set("缓存大小必须为数字")
      return None
    if mem_size < 0:
        hint_info.set("缓存大小不能小于零")
        return None

    data['sysArgs']['gsExecPath'] = path_args['grads_exec_path'].get()
    data['sysArgs']['gsDataPath'] = path_args['ncep_data_path'].get()
    data['sysArgs']['gsDocPath'] = path_args['img_doc_path'].get()
    data['sysArgs']['maxDocSize'] = max_mem_size.get()

    data_file = open(data['sysArgs']['argDataFile'], 'wb')
    pickle.dump(data['sysArgs'], data_file)
    data_file.close()

    # do the arg change
    MemManager(
        doc_path=self.dataStream['sysArgs']['gsDocPath'],
        max_mem=self.dataStream['sysArgs']['maxDocSize']
        )

    # close the arg_config window
    master.withdraw()

  def _MakeMenu( self, master, texts ):
    """
    texts is [('name', func), ('name', [('name', func)])]
    """
    self.logger.info(
        '._MakeMenu(master=%s, texts=%s)' % (repr(master), repr(texts))
        )

    for main_menu in texts:
      if (isinstance(main_menu[1], types.FunctionType)
          or isinstance(main_menu[1], types.MethodType)):
        command = partial(main_menu[1], main_menu[0])
        master.add_command(label=main_menu[0], command=command)
      elif isinstance(main_menu[1], types.ListType):
        child_menu = Menu(master)
        master.add_cascade(label=main_menu[0], menu=child_menu)
        self._MakeMenu( master=child_menu, texts=main_menu[1] )
      else:
        self.logger.error( "002 texts: %s" % repr(texts) )
        raise WidgetError( 002,  "_MakeMenu texts should be list or function" )


class Toolbar( Frame ):

  def __init__( self, master, dataStream ):
    Frame.__init__(self, master)

    self.dataStream = dataStream

    self.logger = logging(
        self.dataStream['sysArgs']['hostPath'], __name__ + '.Toolbar'
        )
    self.logger.info(
        ".__init__(master=%s, dataStream=%s)"
        % (repr(master), repr(dataStream))
        )

    # check the icons
    iconsPath = os.path.join(
        self.dataStream['sysArgs']['hostPath'], 'icons'
        )
    if not os.path.isdir(iconsPath):
      self.logger.error( '101:not found iconsPath: %s' % repr(iconsPath) )
      raise WidgetError( 101, 'not found iconsPath: %s' % repr(iconsPath) )

    try:
      icon_left = Image.open(os.path.join(iconsPath, 'left.jpg'))
      icon_right = Image.open(os.path.join(iconsPath, 'right.jpg'))
      icon_up = Image.open(os.path.join(iconsPath, 'up.jpg'))
      icon_down =  Image.open(os.path.join(iconsPath, 'down.jpg'))
    except IOError, e:
      self.logger.error( '102:icon file error: %s' % repr(e) )
      raise WidgetError( 102, 'icon file error: %s' % repr(e) )

    icon_left = ImageTk.PhotoImage(icon_left)
    icon_right = ImageTk.PhotoImage(icon_right)
    icon_up = ImageTk.PhotoImage(icon_up)
    icon_down = ImageTk.PhotoImage(icon_down)

    self.icons = [icon_left, icon_right, icon_up, icon_down]

  def draw( self , funcs):
    """
    draw the toolbar
    """
    self.logger.info( ".draw(funcs=%s)" % repr(funcs) )

    self.funcs = funcs

    command = partial(self.hide_sidebar, funcs['argsCheckBar'])
    Button(self, text="侧栏", command=command).pack(side=LEFT, fill=Y)

    up = partial(self.pagechange, 'up')
    down = partial(self.pagechange, 'down')
    forward = partial(self.pagechange, 'forward')
    backward = partial(self.pagechange, 'backward')

    Button(self, image=self.icons[0], command=backward).pack(side=LEFT)
    Button(self, image=self.icons[1], command=forward).pack(side=LEFT)
    Button(self, image=self.icons[2], command=up).pack(side=LEFT)
    Button(self, image=self.icons[3], command=down).pack(side=LEFT)

    Button(
        self, text="复制", command=self.export2clipboard
        ).pack(side=LEFT, fill=Y)
    Button(
        self, text='显示图片', command=self._ShowPic
        ).pack(side=LEFT, fill=Y)

    Label(
        self, textvariable=self.dataStream['posterStatus']['hintInfo'][1],
        fg='brown', font=("ComicSans", '10', 'bold')
        ).pack(side=RIGHT, fill=X)

  def _ShowPic( self ):
    self.logger.info( "_ShowPic" )

    if not self.dataStream['posterStatus']['posterAlbum']['main'][1]:
      return None
    th = Thread(
        target=self.dataStream['posterStatus']['posterAlbum']['main'][1].show
        )
    th.start()

  def pagechange( self, orient='forward', event=None ):
    """
    when toolbar's button be clicked, change the Poster's image
    orient should be "down/up/forward/backward"
    """
    self.logger.info(
        ".pagechange( orient=%s, event=%s )"
        % (repr(orient), repr(event))
        )

    sidebar = self.funcs['sidebar']
    data = self.dataStream['phyArgs']

    # <time change>
    if orient == 'forward' or orient == 'backward':
      year = int(data['year'][0])
      month = int(data['month'][0])
      day = int(data['day'][0])
      time = int(data['time'][0])
      the_datetime = datetime.datetime(year, month, day, time, 0, 0)

      delta = ''
      if orient == 'forward': delta = 6 * 60 * 60
      elif orient == 'backward': delta = -6 * 60 * 60

      the_datetime = the_datetime + datetime.timedelta(seconds=delta)
      data['year'][1].set(IntStr(the_datetime.year, 2))
      data['month'][1].set(IntStr(the_datetime.month, 2))
      data['day'][1].set(IntStr(the_datetime.day, 2))
      data['time'][1].set(IntStr(the_datetime.hour, 2))
    # </time change>

    # <level change>
    elif orient == 'up' or orient == 'down':
      if not data['whether_custom'][0]: return None
      the_lev = data['high'][0].strip()

      if orient == "up":
        if the_lev == '100': return None
        elif the_lev =='850': the_lev = 700
        elif the_lev == '地面': the_lev = 850
        else:
          the_lev = int(the_lev) - 100
      elif orient == 'down':
        if the_lev == '地面': return None
        elif the_lev == '700': the_lev = 850
        elif the_lev == '850': the_lev = '地面'
        else:
          the_lev = int(the_lev) + 100

      if the_lev != '地面': the_lev = str(the_lev) + ' '
      data['high'][1].set(the_lev)
    # </level change>

    sidebar._DrawCanvas()

  def shuchu( self, event=None ):
    print 'not found'

  def export2clipboard( self, event=None ):
    """
    export image to clicboard
    """
    self.logger.info( ".export2clipboard(event=%s)" % repr(event) )

    if not self.dataStream['posterStatus']['posterAlbum']['main'][1]:
      return None
    img = self.dataStream['posterStatus']['posterAlbum']['main'][1]
    output = StringIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

  def hide_sidebar( self, side_bar, event=None ):
    """
    hide or display the side_bar
    """
    self.logger.info(
        ".hide_sidebar(side_bar=%s, event=%s)" % (repr(side_bar), repr(event))
        )

    try:
      side_bar[0].pack_info()
      side_bar[0].pack_forget()
    except:
      side_bar[1].pack_forget()
      side_bar[0].pack(side=LEFT, fill=BOTH)
      side_bar[1].pack(side=LEFT, fill=BOTH, expand=True)


class ArgsCheckBar( Frame ):

  def __init__( self, master, dataStream ):
    Frame.__init__(self, master)
    self.logger = logging(
        dataStream['sysArgs']['hostPath'], __name__ + '.ArgsCheckBar'
        )

    self.logger.info(
        '.__init__(master=%s, dataStream=%s)' % (repr(master), repr(dataStream))
        )

    self.dataStream = dataStream

    #self.config(highlightbackground='#435066', highlightthickness=1, bd=1)

  def draw( self, hisTexts, Poster, Makegs):
    """
    draw the args' check bar on the left
    """
    self.logger.info(
        '.draw(hisTexts=%s, Poster=%s, Makegs=%s)'
        % (repr(hisTexts), repr(Poster), repr(Makegs))
        )

    self.hisTexts = hisTexts
    self.Poster = Poster
    self.GsMaker = Makegs

    self.argsMessage = StringVar()
    self.argsMessage.set('')

    Label(
        self, text='---------------日期---------------',
        fg='brown'
        ).grid(row=1, column=0, columnspan=5, sticky=EW)

    rb1 = Radiobutton(
        self, text='历史案例',
        variable=self.dataStream['phyArgs']['whether_historia'][1],
        value=1, command=self._RadioLock
        )
    rb1.grid(row=3, column=1, columnspan=2, sticky=W)

    Button(
        self, text=' 个例谱查询 ', width=10, command=self._HistoriaSel
        ).grid(row=3, column=3, columnspan=2, sticky=W)

    wds1 = Entry(
        self, textvariable=self.dataStream['phyArgs']['year'][1],
        width=5
        )
    wds1.grid(row=5, column=1, sticky=E)
    Label(self, text='年').grid(row=5, column=2, sticky=EW)
    months = [i for i in range(1, 12)]
    wds2 = OptionMenu(
        self, self.dataStream['phyArgs']['month'][1], *months,
        command=self._UpdateHistoria
        )
    wds2.grid(row=5, column=3, sticky=EW)
    Label(self, text='月').grid(row=5, column=4, sticky=EW)

    exms = self._HistoriaCheck( hisTexts )
    self.dataStream['phyArgs']['historia'][1].set(exms[0])
    self.dataStream['phyArgs']['historia'][0] = exms[0]
    # there is a copy if wds3 in _UpdateHistoria
    wds3 = OptionMenu(
        self, self.dataStream['phyArgs']['historia'][1], *exms,
        command=self._UpdateHistoria
        )
    wds3.grid(row=7, column=1, columnspan=4, sticky=EW)

    self.historiaWidges = [wds1, wds2, wds3]

    rb2 = Radiobutton(
        self, text='自选日期',
        variable=self.dataStream['phyArgs']['whether_historia'][1],
        value=0, command=self._RadioLock
        )
    rb2.grid(row=9, column=1, columnspan=4, sticky=W)
    wds4 = Entry(
        self, textvariable=self.dataStream['phyArgs']['year'][1],
        width=5
        )
    wds4.grid(row=11, column=1, sticky=E)
    Label(self, text='年').grid(row=11, column=2, sticky=EW)
    months = [i for i in range(1, 12)]
    wds5 = OptionMenu(
        self, self.dataStream['phyArgs']['month'][1], *months,
        command=self._UpdateHistoria
        )
    wds5.grid(row=11, column=3, sticky=EW)
    Label(self, text='月').grid(row=11, column=4, sticky=EW)

    wds6 = Entry(
        self, textvariable=self.dataStream['phyArgs']['day'][1],
        width=5
        )
    wds6.grid(row=13, column=1, sticky=E)
    Label(self, text='日').grid(row=13, column=2, sticky=EW)
    times = ['00', '06', '12', '18']
    wds7 = OptionMenu(
        self, self.dataStream['phyArgs']['time'][1], *times
        )
    wds7.grid(row=13, column=3, sticky=E)
    Label(self, text='时').grid(row=13, column=4, sticky=EW)

    self.cusDataWidgets = [wds4, wds5, wds6, wds7]

    Label(
        self, text='-------------绘图区域-------------',
        fg='brown',
        ).grid(row=15, column=1, columnspan=5, sticky=EW)

    Label(self, text='经度').grid(row=17, column=1, sticky=EW)
    Entry(
        self, textvariable=self.dataStream['phyArgs']['lon_fr'][1],
        width=5
        ).grid(row=17, column=2, sticky=E)
    Label(self, text='到').grid(row=17, column=3, sticky=EW)
    Entry(
        self, textvariable=self.dataStream['phyArgs']['lon_to'][1],
        width=5
        ).grid(row=17, column=4, sticky=E)

    Label(self, text='纬度').grid(row=19, column=1, sticky=EW)
    Entry(
        self, textvariable=self.dataStream['phyArgs']['lat_fr'][1],
        width=5
        ).grid(row=19, column=2, sticky=E)
    Label(self, text='到').grid(row=19, column=3, sticky=EW)
    Entry(
        self, textvariable=self.dataStream['phyArgs']['lat_to'][1],
        width=5
        ).grid(row=19, column=4, sticky=E)

    Label(
        self, text='-------------参数选择-------------',
        fg='brown'
        ).grid(row=21, column=1, columnspan=5, sticky=EW)

    rb3 = Radiobutton(
        self,
        variable=self.dataStream['phyArgs']['whether_custom'][1],
        value=0, command=self._RadioLock
        )
    rb3.grid(row=23, column=1, sticky=W)
    args = self.dataStream['phyArgs']['args'][1][1]
    wds8 = OptionMenu(
        self, self.dataStream['phyArgs']['multi'][1], *args,
        command=self._ArgsSyn
        )
    wds8.grid(row=23, column=2, columnspan=3, sticky=EW)

    self.argsWidgets = [wds8]

    rb4 = Radiobutton(
        self,
        variable=self.dataStream['phyArgs']['whether_custom'][1],
        value=1, command=self._RadioLock
        )
    rb4.grid(row=25, column=1, sticky=W)
    levels = [str(i) + ' ' for i in range(100, 800, 100)]
    levels += ['850 ', '地面']
    wds9 = OptionMenu(
        self, self.dataStream['phyArgs']['high'][1], *levels,
        command=self._UpdateArgs
        )
    wds9.grid(row=25, column=2, sticky=EW)
    self.dataStream['phyArgs']['args'][0].set(
        self.dataStream['phyArgs']['args'][1][0][0]
        )
    wds10 = OptionMenu(
        self, self.dataStream['phyArgs']['args'][0],
        *self.dataStream['phyArgs']['high_args'],
        command=self._ArgsSyn
        )
    wds10.grid(row=25, column=3, columnspan=2, sticky=EW)

    self.cusArgsWidgets = [wds9, wds10]

    Label(self, text='').grid(row=49)

    Label(
        self, textvariable=self.argsMessage, fg='red'
        ).grid(row=50, column=1, columnspan=3, sticky=EW)
    Button(
        self, text='确认绘图', command=self._DrawCanvas
        ).grid(row=50, column=4, sticky=EW)

    # initialled
    rb1.select()
    rb3.select()
    self._RadioLock()
    self.widgets = [wds1, wds2, wds3, wds4, wds5, wds6, wds7, wds8, wds9, wds10]

  def _HistoriaSel( self, event=None ):
    """
    open a window to select historia data
    """
    self.logger.info( '_HistoriaSel(event=%s)' % repr(event) )
    if self.dataStream['historia']['histexts_win']: return None

    data = self.dataStream
    root = data['historia']['root']

    master = Toplevel()

    # <set Tk_Var>
    cate = StringVar()
    year = IntVar()
    month = StringVar()
    hint_info = StringVar()
    list_var = StringVar()

    cate.set('全部  ')
    year.set(0)
    month.set('全部')
    hint_info.set('')
    list_var.set('')

    self.his_sel_arg = {
        'cate': cate,
        'year': year,
        'month': month,
        'hint_info': hint_info,
        'list_var': list_var,
        }
    # </set Tk_Var>

    # <set the historia select window>
    screen_size = [root.winfo_screenwidth(), root.winfo_screenheight()]
    size = [600, 600]
    master.minsize(*size)
    master.resizable(False, False)
    master.transient(root)
    master.title('个例谱查询')
    master.geometry(
        "%sx%s+%s+%s"
        % (
              size[0], size[1],
              (screen_size[0] - size[0]) / 2,
              (screen_size[1] - size[0]) / 2
          )
        )
    # </set the historia select window>

    frame_top = Frame(master)
    frame_down = Frame(master)
    frame_his = Frame(frame_down)

    frame_top.pack(fill=BOTH)
    frame_down.pack(fill=BOTH, expand=True)

    try:
      with open(
          os.path.join(data['sysArgs']['hostPath'], 'historia.dat')
          ) as his_data_file:
        his_data = pickle.load(his_data_file)
    except:
      return None

    # <args select texts geomanager>
    grid_row = 0
    grid_column = 0
    Label(frame_top, text='  ').grid(row=grid_row, column=grid_column)

    grid_row += 1
    grid_column += 1
    Label(
        frame_top, text='类别：', fg='brown'
        ).grid(row=grid_row, column=grid_column, sticky=E)
    grid_column += 1
    cates = ['全部  ', '暴风雪', '雪灾  ', '沙尘  ']
    OptionMenu(
        frame_top, self.his_sel_arg['cate'],
        *cates, command=self._HisSelCheck
        ).grid(row=grid_row, column=grid_column)

    grid_column += 1
    Label(frame_top, text='  ').grid(row=grid_row, column=grid_column)

    grid_column += 1
    Entry(
        frame_top, textvariable=self.his_sel_arg['year'],
        width=10
        ).grid(row=grid_row, column=grid_column)
    grid_column += 1
    Label(frame_top, text='年').grid(row=grid_row, column=grid_column)

    grid_column += 1
    Label(frame_top, text='  ').grid(row=grid_row, column=grid_column)

    months = [IntStr(i, 2)+ '  ' for i in range(1, 13)]
    months.append('全部')
    grid_column += 1
    OptionMenu(
        frame_top, self.his_sel_arg['month'],
        *months, command=self._HisSelCheck
        ).grid(row=grid_row, column=grid_column)
    grid_column += 1
    Label(frame_top, text='月').grid(row=grid_row, column=grid_column)

    grid_column += 1
    Label(frame_top, text='  ').grid(row=grid_row, column=grid_column)

    grid_column += 1
    Button(
        frame_top, text='  查询  ',
        command=self._HisSelSeek
        ).grid(row=grid_row, column=grid_column)

    grid_column += 1
    Label(
        frame_top, textvariable=self.his_sel_arg['hint_info'],
        fg='red'
        ).grid(row=grid_row, column=grid_column, columnspan=2, sticky=E)

    grid_row += 1
    grid_column += 1
    Label(frame_top, text='  ').grid(row=grid_row, column=grid_column)
    # </args select texts geomanager>

    Label(frame_down, text='  ').grid(row=1, column=0)
    Label(frame_down, text='  ').grid(row=2, column=2)

    # <historia texts set>
    frame_his.grid(row=1, column=1)

    frame_his_up = Frame(frame_his)
    frame_his_down = Frame(frame_his)
    frame_his_up.pack(expand=True, fill=BOTH)
    frame_his_down.pack(fill=BOTH)

    his_list = Listbox(frame_his_up, width=90, height=38)
    scroll_y = Scrollbar(frame_his_up)
    scroll_x = Scrollbar(frame_his_down)

    his_list.config(xscrollcommand=scroll_x.set)
    his_list.config(yscrollcommand=scroll_y.set)
    scroll_x.config(command=his_list.xview, orient=HORIZONTAL)
    scroll_y.config(command=his_list.yview)

    list_var = self.his_sel_arg['list_var']
    his_list.config(listvariable=list_var)
    his_list.bind('<Double-Button-1>', self._HisClick)

    his_list.pack(side=LEFT, expand=True, fill=BOTH)
    scroll_y.pack(side=LEFT, fill=BOTH)
    scroll_x.pack(fill=BOTH)
    self.his_list = his_list
    # </historia texts set>

  def _HisClick( self, event=None ):
    """
    double click the historia text then change the phyArgs
    """
    self.logger.info( '._HisClick(event=%s)' % repr(event) )

    his_text = self.his_list.get(self.his_list.curselection())

    year = int(his_text[: 4])
    month = int(his_text[his_text.index('年')+1: his_text.index('月')])
    day = int(his_text[his_text.index('月')+1: his_text.index('月')+3])

    data = self.dataStream['phyArgs']

    data['year'][1].set(year)
    data['month'][1].set(month)
    data['day'][1].set(day)

    self.dataStream.synchro()

  def _HisSelCheck( self, event=None ):
    """
    check the hisSel window's argument
    """
    self.logger.info( '_HisSelCheck(event=%s)' % repr(event) )

    self.his_sel_arg['hint_info'].set('')

    try:
      self.his_sel_arg['year'].get()
    except ValueError:
      self.his_sel_arg['hint_info'].set('年数必须为整数')
      return None

    if self.his_sel_arg['year'].get() < 0:
      self.his_sel_arg['hint_info'].set('年数必须为正数')
      return None

    return True

  def _HisSelSeek(self, event=None):
    """
    draw the historic texts
    """
    self.logger.info( '_HisSelSeek(event=%s)' % repr(event) )

    data = self.dataStream

    if not self._HisSelCheck():
      return None

    his_data_path = os.path.join(data['sysArgs']['hostPath'], 'historia.dat')
    his_data_path = PathSwitch( his_data_path )
    if not os.path.isfile(his_data_path):
      return None

    try:
      with open(his_data_path, 'rb') as his_data_file:
        his_data = pickle.load(his_data_file)
    except:
      self.his_sel_arg['hint_info'].set('个例谱数据文件异常')
      return None

    cate_dic = {
        '暴风雪': 'blizzard',
        '雪灾': 'snow',
        '沙尘': 'sand',
        }

    ans = []

    sel_cate = self.his_sel_arg['cate'].get().strip()
    sel_year = self.his_sel_arg['year'].get()
    sel_month = self.his_sel_arg['month'].get().strip()

    if sel_cate == '全部':
      the_cate = cate_dic.values()
    else:
      the_cate = [cate_dic[sel_cate]]
    the_cate.sort()

    if sel_year == 0:
      the_year = []
      for cate in his_data:
        the_year += his_data[cate].keys()
        the_year = list(set(the_year))
        the_year.sort()
    else:
      the_year = [sel_year]

    if sel_month == '全部':
      the_month = [i for i in range(1, 13)]
    else:
      the_month = [int(sel_month)]

    for cate in the_cate:
      if cate not in his_data: continue

      for year in the_year:
        if year not in his_data[cate]: continue

        for month in the_month:
          if month not in his_data[cate][year]: continue

          texts = his_data[cate][year][month]

          for each_text in texts:
            the_ans = str(year) + '年' + IntStr(month, 2) + '月'
            the_ans += '__'.join(each_text.strip().split('\t'))
            ans.append(the_ans)

    ans = ' '.join(ans)
    self.his_sel_arg['list_var'].set(ans)

  def _UpdateArgs( self, event=None ):
    """
    update the custom args to adapt for the level
    """
    self.logger.info( '._UpdateArgs()' )

    data = self.dataStream
    self._ArgsSyn()

    if data['phyArgs']['high'][0] == '地面':
      arg_list = data['phyArgs']['surf_args']
    else: arg_list = data['phyArgs']['high_args']

    wds10 = self.widgets[9]
    wds10.pack_forget()
    if data['phyArgs']['args'][0].get() not in arg_list:
      data['phyArgs']['args'][0].set(arg_list[0])
    wds10 = OptionMenu(
        self, data['phyArgs']['args'][0],
        *arg_list,
        command=self._ArgsSyn
        )
    wds10.grid(row=25, column=3, columnspan=2, sticky=EW)
    self.widgets[9] = wds10

  def _DrawCanvas( self ):
    """
    use args to draw the picture
    """
    self.logger.info( '._DrawCanvas()' )
    data = self.dataStream['phyArgs']

    bool_res = self._ArgsSyn()
    if not bool_res: return None

    self.argsMessage.set('正在尝试绘图...')

    # define the image's name
    arg_change = {
        '温度': 'tt',
        '高度': 'height',
        '相对湿度': 'rh',
        '风场': 'wind',
        '地面气压': 'sfcg',
        '抬升指数': 'lftx',
        '水汽含量': 'prwtr',
        '海平面气压': 'slp',
        '绝对湿度': 'shum',
        '500 高度 & 850h uv & rh': '500hPa.Height.&.850hPa.Wind.&.850hPa.RH',
        '700 风场 & 700 相对湿度': '700hPa.Wind.&.700hPa.RH',
        '850 风场 & 850 相对湿度': '850hPa.Wind.&.850hPa.RH',
        '500 高度 & 850 温度': '500hPa.Height.&.850hPa.TT',
        }
    if self.dataStream['phyArgs']['whether_custom'][0]:
      the_arg = self.dataStream['phyArgs']['args'][0].get().strip()
      if the_arg in arg_change:
        the_arg = arg_change[the_arg]
    else:
      the_arg = self.dataStream['phyArgs']['multi'][0].strip()
      if the_arg in arg_change:
        the_arg = arg_change[the_arg]

    if '地面' in self.dataStream['phyArgs']['high'][0]:
      the_level = 'Pre1000_'
    else:
      the_level = self.dataStream['phyArgs']['high'][0].strip()
      the_level = 'Pre' + the_level + '_'

    if not self.dataStream['phyArgs']['whether_custom'][0]:
      the_level = ''

    data = self.dataStream['phyArgs']
    the_time = (
        IntStr( data['year'][0], 4 )
        + IntStr( data['month'][0], 2 )
        + IntStr( data['day'][0], 2 ) + '_'
        + IntStr( data['time'][0], 2 )
        )
    self.dataStream['posterStatus']['img_name'] = (
        "NCEP_" + the_level + the_arg + '_'
        + the_time + "_(%s,%s,%s,%s)"
        % (data['lon_fr'][0], data['lon_to'][0],
           data['lat_fr'][0], data['lat_to'][0])
        + '.gif'
        )
    # draw the canvas
    img_path = ''
    start_time = time.time()

    while True:
      try:
        if time.time() - start_time > 3: break
        self.GsMaker.config_NCEP( self.dataStream )
        self.GsMaker.makefile()
        img_path = self.GsMaker.draw()
        break
      except Exception, e:
        print repr(e)
        continue

    if not img_path:
      self.argsMessage.set("绘图失败")
      return None
    else:
        self.dataStream.update()
        self.argsMessage.set("绘图成功")

    # <display hint info>
    if self.dataStream['phyArgs']['whether_custom'][0]:
      if '地面' not in self.dataStream['phyArgs']['high'][0]:
        args = self.dataStream['phyArgs']['high'][0].strip() \
               + 'hPa ' \
               + self.dataStream['phyArgs']['args'][0].get()
      else:
        args = self.dataStream['phyArgs']['high'][0].strip() \
               + ' ' \
               + self.dataStream['phyArgs']['args'][0].get()
    else:
      args = self.dataStream['phyArgs']['multi'][0]

    self.dataStream['posterStatus']['hintInfo'][1].set(
        self.dataStream['phyArgs']['year'][0].__str__() + '年'
        + self.dataStream['phyArgs']['month'][0].__str__() + '月'
        + self.dataStream['phyArgs']['day'][0].__str__() + '日'
        + self.dataStream['phyArgs']['time'][0].__str__() + '时 '
        + args
        )
    # </display hint info>

    MemManager(
        doc_path=self.dataStream['sysArgs']['gsDocPath'],
        max_mem=self.dataStream['sysArgs']['maxDocSize']
        )

    mtime = time.mktime(datetime.datetime.now().timetuple())
    os.utime(img_path, (mtime, mtime))
    self.dataStream.update()

    self.Poster.draw( image_path=img_path )

  def _ArgsCheck( self, event=None ):
    """
    check the input args
    if they are correct, draw the picture
    """
    self.logger.info( '._ArgsCheck(event=%s)' % repr(event) )

    data = self.dataStream['phyArgs']
    try:
      data['year'][1].get()
      data['day'][1].get()
      data['time'][1].get()
      data['lon_fr'][1].get()
      data['lon_to'][1].get()
      data['lat_fr'][1].get()
      data['lat_to'][1].get()
    except ValueError:
      self.argsMessage.set('参数必须为整数')
      return None

    if data['year'][1].get() < 1990:
      self.argsMessage.set('年数必须大于1990')
      return None
    if data['year'][1].get > datetime.date.today().year:
      self.argsMessage.set('年数不得大于%s' % datetime.date.today().year)

    dayrange = calendar.monthrange(
        data['year'][1].get(), data['month'][1].get()
        )[1]
    if data['day'][1].get() > dayrange:
      self.argsMessage.set('日数必须小于%s' % dayrange)
      return None

    if (data['lon_fr'][1].get() >= data['lon_to'][1].get()
        or data['lon_fr'][1].get() < 0):
      self.argsMessage.set('经度输入错误')
      return None

    if (data['lat_fr'][1].get() >= data['lat_to'][1].get()
        or data['lat_fr'][1].get() < 0):
      self.argsMessage.set('纬度输入错误')
      return None

    if self.dataStream['phyArgs']['whether_historia'][1].get():
      if '日' not in self.dataStream['phyArgs']['historia'][1].get():
        self.argsMessage.set('请选择一个历史个例')
        return None

    if self.dataStream['phyArgs']['day'][1].get() < 1:
      self.argsMessage.set('天数不能小于1')
      return None

    self.argsMessage.set('')
    return True

  def _UpdateHistoria( self, event=None ):
    """
    update the historia example
    """
    self.logger.info( '._UpdateHistoria(event=%s)' % repr(event) )

    self._ArgsSyn()

    wds = self.historiaWidges[2]
    wds.grid_remove()

    exms = self._HistoriaCheck( self.hisTexts )
    if '刷新' not in exms: exms.append('刷新')
    if (self.dataStream['phyArgs']['historia'][0] not in exms
        or self.dataStream['phyArgs']['historia'][0] == '刷新'):
      self.dataStream['phyArgs']['historia'][1].set(exms[0])
    wds3 = OptionMenu(
        self, self.dataStream['phyArgs']['historia'][1], *exms,
        command=self._UpdateHistoria
        )
    wds3.grid(row=7, column=1, columnspan=4, sticky=EW)
    self.historiaWidges[2] = wds3

    if '日' in self.dataStream['phyArgs']['historia'][0]:
      index = self.dataStream['phyArgs']['historia'][0].index('日')
      the_day = self.dataStream['phyArgs']['historia'][0][: index]
      if '-' in the_day: the_day = the_day[: the_day.index('-')]
      self.dataStream['phyArgs']['day'][1].set(int(the_day))
    self._ArgsSyn()

  def _HistoriaCheck( self, hisTexts, ):
    """
    return the historic data
    """
    self.logger.info( '._HistoriaCheck(hisTexts=%s)' % repr(hisTexts) )

    self._ArgsSyn()

    year = self.dataStream['phyArgs']['year'][0]
    month = self.dataStream['phyArgs']['month'][0]
    if year in hisTexts:
      if month in hisTexts[year]:
        self.logger.info(
            '_HistoriaCheck return %s' %  repr(hisTexts[year][month])
            )
        if '刷新' not in hisTexts[year][month]:
          hisTexts[year][month].append('刷新')
        return hisTexts[year][month]

    self.logger.info(
        '_HistoriaCheck reutrn %s' % repr(['该月没有历史个例'])
        )
    return ['该月没有历史个例']

  def _RadioLock( self ):
    """
    set the another radiobutton's state to DISABLED
    """
    self.logger.info( '._RadioLock()' )

    bool_historia = self.dataStream['phyArgs']['whether_historia'][1].get()
    self._ArgsSyn()

    if bool_historia == 1:
      for each_wds in self.historiaWidges:
        each_wds.config(state=NORMAL)
      for each_wds in self.cusDataWidgets:
        each_wds.config(state=DISABLED)
    elif bool_historia == 0:
      for each_wds in self.historiaWidges:
        each_wds.config(state=DISABLED)
      for each_wds in self.cusDataWidgets:
        each_wds.config(state=NORMAL)

    bool_args = self.dataStream['phyArgs']['whether_custom'][1].get()

    if bool_args == 1:
      for each_wds in self.argsWidgets:
        each_wds.config(state=DISABLED)
      for each_wds in self.cusArgsWidgets:
        each_wds.config(state=NORMAL)
    elif bool_args == 0:
      for each_wds in self.argsWidgets:
        each_wds.config(state=NORMAL)
      for each_wds in self.cusArgsWidgets:
        each_wds.config(state=DISABLED)

  def _ArgsSyn( self, event=None ):
    """
    synchro the dataStream
    """
    self.logger.info( '._ArgsSyn(event=%s)' % repr(event) )

    bool_arg = self._ArgsCheck()

    for cate in self.dataStream:
      for key in self.dataStream[cate]:
        if not isinstance(self.dataStream[cate][key], types.ListType):
          continue
        if not (isinstance(self.dataStream[cate][key][1], StringVar)
                or isinstance(self.dataStream[cate][key][1], IntVar)):
          continue
        try:
          self.dataStream[cate][key][0] = self.dataStream[cate][key][1].get()
        except: pass

    self.logger.debug( repr(self.dataStream) )
    if not bool_arg: return None
    return True


class FileList( Frame ):

  def __init__( self, master, dataStream ):
    Frame.__init__(self, master)

    self.logger = logging(
        dataStream['sysArgs']['hostPath'], __name__ + '.FileList'
        )

    self.logger.info(
        '.__init__(master=%s, dataStream=%s)'
        % (repr(master), repr(dataStream))
        )

    self.dataStream = dataStream

    frame_top = Frame(self)
    frame_up = Frame(self)
    frame_down = Frame(self)

    frame_top.pack(fill=BOTH)
    frame_up.pack(expand=True, fill=BOTH)
    frame_down.pack(fill=BOTH)

    label = Label(
        frame_top, text='-------------操作历史-------------',
        fg='brown'
        ).pack(fill=BOTH)
    listbox = Listbox(frame_up)
    scroll_x = Scrollbar(frame_down)
    scroll_y = Scrollbar(frame_up)

    listbox.config(xscrollcommand=scroll_x.set)
    listbox.config(yscrollcommand=scroll_y.set)
    scroll_x.config(command=listbox.xview, orient=HORIZONTAL)
    scroll_y.config(command=listbox.yview)

    listbox.pack(side=LEFT, expand=True, fill=BOTH)
    scroll_y.pack(side=RIGHT, fill=BOTH)
    scroll_x.pack(fill=BOTH)

    listVar = self.dataStream['posterStatus']['fileList'][1]
    listbox.config(listvariable=listVar)
    listbox.bind('<Double-Button-1>', self._FileClick)

    self.listbox = listbox

  def draw( self, thePoster=None ):
    """
    draw the listbox of doc res
    """
    self.logger.info( '.draw(thePoster=%s)' % repr(thePoster) )

    data = self.dataStream
    self.Poster = thePoster

    data.update()

  def _FileClick( self, event=None ):
    """
    double click the filename then open the historic image
    """
    self.logger.info( '._FileClick(event=%s)' % repr(event) )

    file_name = self.listbox.get(self.listbox.curselection())
    file_path = os.path.join(
        self.dataStream['sysArgs']['gsDocPath'], file_name
        )

    mtime = time.mktime(datetime.datetime.now().timetuple())
    os.utime(file_path, (mtime, mtime))

    self.Poster.draw( image_path=file_path )
    self.dataStream.update()


class Poster( Canvas ):

  def __init__( self, master, dataStream ):
    Canvas.__init__(self, master)

    self.dataStream = dataStream
    self.master = master

    self.logger = logging(
        dataStream['sysArgs']['hostPath'], __name__ + '.PosterBoard'
        )
    self.logger.info(
        '.__init__(master=%s, dataStream=%s)' % (repr(master), repr(dataStream))
        )

    self.config(bd=0, highlightbackground='#435066', highlightthickness=1,
                bg='#363636')

    back_ground_path = os.path.join(
        dataStream['sysArgs']['hostPath'], 'icons', 'background.jpg'
        )
    back_ground_path = PathSwitch( back_ground_path )
    if not os.path.isfile(back_ground_path):
      self.logger.error(
          "203:back_ground_path not found: %s" % back_ground_path
          )
      raise WidgetError(
          203, "back_ground_path not found: %s" % back_ground_path
          )

    height = self.winfo_height()
    width = self.winfo_width()

    back_ground_img = Image.open(back_ground_path)
    self.dataStream['posterStatus']['posterAlbum']['back'][1] = back_ground_img

    back_ground_img = back_ground_img.copy()
    back_ground_img = back_ground_img.resize((width, height))
    back_ground_pic = ImageTk.PhotoImage(back_ground_img)
    self.dataStream['posterStatus']['posterAlbum']['back'][0] = back_ground_pic

    img_id = self.create_image(width/2, height/2, image=back_ground_pic)
    self.dataStream['posterStatus']['posterAlbum']['back'][2] = img_id
    self.bind('<Configure>', self._Resize)

  def draw( self, image_path=None, image=None ):
    """
    draw the poster canvas
    image is a PIL.Image instance
    ---------
    update the image size use the image
    new canvas_image use the image_path
    """
    self.logger.info(
        '.draw(image_path=%s, image=%s)'
        % (repr(image_path), repr(image))
        )

    try:
      self.delete(
          self.dataStream['posterStatus']['posterAlbum']['main'][2]
          )
    except: pass

    if image_path:
      if not os.path.isfile(image_path):
        self.logger.error( '201 imagefile=%s' % repr(image_path) )
        raise WidgetError(
            201, 'not existed. imagefile=%s' % repr(image_path)
            )

      try:
        image = Image.open(image_path)
        self.dataStream['posterStatus']['posterAlbum']['main'][1] = image
        image = image.copy()
        image = image.convert('RGB')
        height = self.winfo_height()
        width = self.winfo_width()
        image.thumbnail((width, height), Image.ANTIALIAS)
      except Exception, e:
        self.logger.error( '202 error:%s' % repr(e) )
        raise WidgetError( 202, 'Image.open error:%s' % repr(e) )

    pic = ImageTk.PhotoImage(image)

    self.dataStream['posterStatus']['posterAlbum']['main'][0] = pic

    height = self.winfo_height()
    width = self.winfo_width()

    img_id = self.create_image(width/2, height/2, image=pic)
    self.dataStream['posterStatus']['posterAlbum']['main'][2] = img_id

  def _Resize( self, event=None ):
    """
    update the image's size
    """
    self.logger.info( '._Resize(event=%s)' % repr(event) )

    height = self.winfo_height()
    width = self.winfo_width()

    # update background
    self.delete(
        self.dataStream['posterStatus']['posterAlbum']['back'][2]
        )
    back = self.dataStream['posterStatus']['posterAlbum']['back'][1]
    back = back.copy()
    back = back.resize((width, height))
    back = ImageTk.PhotoImage(back)
    self.dataStream['posterStatus']['posterAlbum']['back'][0] = back
    img_id = self.create_image(width/2, height/2, image=back)
    self.dataStream['posterStatus']['posterAlbum']['back'][2] = img_id

    # update the poster image
    if not self.dataStream['posterStatus']['posterAlbum']['main'][1]:
      return None
    image = self.dataStream['posterStatus']['posterAlbum']['main'][1]
    image = image.copy()
    image = image.convert('RGB')
    image.thumbnail((width, height), Image.ANTIALIAS)

    self.draw(image=image)


