#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
from Tkinter import *
import os
import sys
import types
import pickle
from makegs import Makegs
from PIL import Image, ImageTk
from myTools import logging
from myTools import MyException
from myTools import PathSwitch
import Widgets



class dataStream( dict ):

  def __init__( self, data ):
    """
    a dataStream manager depend on python's dict
    """
    dict.__init__( self, data )

    # initialled the Tkinter *Var
    for cate in self:
      for arg in self[cate]:
        if not isinstance(self[cate][arg], types.ListType): continue
        if len(self[cate][arg]) < 2: continue
        if not (isinstance(self[cate][arg][1], IntVar)
                or isinstance(self[cate][arg][1], StringVar)): continue
        value = self[cate][arg][0]
        self[cate][arg][1].set(value)

  def synchro( self ):
    """
    synchro the dataStream
    from Tkinter *Var to string/int
    """

    for cate in self:
      for key in self[cate]:
        if not isinstance(self[cate][key], types.ListType):
          continue
        if not (isinstance(self[cate][key][1], StringVar)
                or isinstance(self[cate][key][1], IntVar)):
          continue
        try:
          self[cate][key][0] = self[cate][key][1].get()
        except: pass

  def dump( self):
    """
    save the sysArgs to arg_data.dat
    """
    file_path = os.path.join(self['sysArgs']['hostPath'], 'arg_data.dat')
    file_path = PathSwitch( file_path )
    data_file = open(file_path, 'wb')
    pickle.dump(self['sysArgs'], data_file)
    data_file.close()

  def load( self ):
    """
    load the sysArgs to arg_data.dat
    """
    file_path = os.path.join(self['sysArgs']['hostPath'], 'arg_data.dat')
    file_path = PathSwitch( file_path )
    data_file = open(file_path, 'rb')
    self['sysArgs'].update(pickle.load(data_file))
    data_file.close()

  def update( self ):
    """
    update the posterStatus' fileList
    """
    path = self['sysArgs']['gsDocPath']
    if not os.path.isdir(path): return None

    gs_files = {}
    for each_file in os.walk(path).next()[2]:
      if os.path.splitext(each_file)[1] != '.gif': continue
      time = os.stat(os.path.join(path, each_file)).st_mtime
      if time in gs_files:
        gs_files[time] = gs_files[time] + ' ' + each_file
      else:
        gs_files.update({time: each_file})

    time_rank = gs_files.keys()
    time_rank.sort(reverse=True)

    list_str = ''
    for each_file in time_rank:
      list_str = list_str + gs_files[each_file] + ' '

    self['posterStatus']['fileList'][0] = list_str
    self['posterStatus']['fileList'][1].set(list_str)


class MainError( MyException ):
  def __init__( self, num, text=None ):
    MyException.__init__( self, num, text )


class NCEPdisplayer():

  def __init__( self, master ):

    # host path
    # pwd = os.path.dirname(sys.executable)
    # pwd = os.path.abspath(os.getcwd())
    pwd = sys.path[0]

    self.root = master

    position = [self.root.winfo_screenwidth(), self.root.winfo_screenheight()]
    position = [int(position[0]/2.-512), int(position[1]/2.-340)]
    size = [1024, 630]
    self.root.geometry(
        "%sx%s+%s+%s"
        % (size[0], size[1], position[0], position[1])
        )
    self.root.state('zoomed')
    self.root.title('NCEP历史资料查询平台')

    self.dataStream = {
        # physical argument
        'phyArgs': {
            'year': [1998, IntVar()], 'month': [2, IntVar()],
            'day': [1, IntVar()], 'time': ['00', StringVar()],
            'high': ['500 ', StringVar()],
            'lon_fr': [30, IntVar()], 'lon_to': [180, IntVar()],
            'lat_fr': [0, IntVar()], 'lat_to': [90, IntVar()],
            'historia': ['刷新', StringVar()],
            'multi': ['500 高度 & 850h uv & rh', StringVar()],
            # makegs.py should update:_ArgSwitch & _SdfOpen
            # Widgets.py should update: _DrawCanvas.arg_change
            'args': [StringVar(), [['高度', '温度', '相对湿度', '风场', 'sfcg', 'sfci',
                                    'lftx', 'prwtr', 'shum', 'slp'],
                                  ['500 高度 & 850h uv & rh',
                                   '700 风场 & 700 相对湿度',
                                   '850 风场 & 850 相对湿度',
                                   '500 高度 & 850 温度    ']]],
            'surf_args': ['高度', '温度', '相对湿度', '风场', '地面气压', '抬升指数',
                          '水汽含量', '海平面气压',],
            'high_args': ['高度', '温度', '相对湿度', '风场', '绝对湿度'],
            'whether_historia': [0, IntVar()],
            'whether_custom': [0, IntVar()],
            },
        'sysArgs': {
            'hostPath': pwd,
            'gsFilePath': os.path.join(pwd, 'gsfile.gs'),
            'gsExecPath': r'X:\GrADS19\win32\grads.exe',
            'gsDataPath': 'X:\\',
            'gsDocPath': os.path.join(pwd, 'images'),
            'maxDocSize': 2.0,
            'argDataFile': os.path.join(pwd, 'arg_data.dat'),
            },
        'posterStatus': {
            'posterAlbum': {'main': ['', '', -1], 'back': ['', '', -1]},
            'hintInfo': ['', StringVar()],
            'img_name': '',
            'fileList': ['', StringVar()],
            },
        'historia':{
            'histexts_win': False,
            'root': self.root,
            }
        }
    self.dataStream = dataStream(self.dataStream)

    #TODO example historic data
    self.hisTexts = {}
    if os.path.isfile(os.path.join(pwd, 'historia.dat')):
      self.hisTexts = pickle.load(
          open(os.path.join(pwd, 'historia.dat'), 'rb')
          )['total']

    self.logger = logging(
        self.dataStream['sysArgs']['hostPath'], __name__
        )
    self.logger.info( '__init__()' )

    # initiall the dataStream
    try:
      self.dataStream.load()
    except IOError:
      pass

    self.logger.debug( repr(self.dataStream) )

  def shuchu( self, var ):
    print var

  def draw( self ):
    self.logger.info( '.draw()' )

    master = self.root

    menu = Widgets.MainMenu( master, self.dataStream )
    toolbar = Widgets.Toolbar( master, self.dataStream )
    board_left = Frame(master)
    board_right = Frame(master)

    sidebar = Widgets.ArgsCheckBar( board_left, self.dataStream )
    filelist = Widgets.FileList(board_left, self.dataStream)
    GsMaker = Makegs()

    menuTexts = [
        ('菜单', [
            ('路径设置', menu.PathConfig),
            ('退出', self.quit),
            ]),
        ]

    menu.draw( menuTexts )
    thePoster = Widgets.Poster( board_right, self.dataStream )

    toolbar.draw(funcs={"argsCheckBar": [board_left, board_right],
                        "sidebar": sidebar})
    toolbar.pack(fill=X)

    sidebar.draw( self.hisTexts, Poster=thePoster, Makegs=GsMaker )
    sidebar.pack(side=TOP, fill=BOTH)
    board_left.pack(side=LEFT, fill=BOTH)
    board_right.pack(side=LEFT, fill=BOTH, expand=TRUE)

    filelist.draw( thePoster=thePoster )
    filelist.pack(fill=BOTH, expand=True)

    thePoster.pack(side=LEFT, expand=True, fill=BOTH)

  def quit( self, event=None ):
    """
    quit app
    """
    self.logger.info( 'quit(event=%s)' % repr(event) )

    self.root.quit()

  def _DataInitial( self, data ):
    """
    initialed the data's TkVar
    """

    for key in data:
      if not isinstance(data[key], types.ListType): continue
      if not (isinstance(data[key][1], IntVar)
              or isinstance(data[key][1], StringVar)): continue
      value = data[key][0]
      data[key][1].set(value)

if __name__ == '__main__':
  master = Tk()
  a = NCEPdisplayer( master )
  a.draw()
  mainloop()