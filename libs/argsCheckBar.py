#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
from Tkinter import *
import os
import sys
import types
import calendar
from functools import partial
from myTools import logging
from myTools import PathSwitch


class ArgsCheckBar( Frame ):
  def __init__( self, master ):
    Frame.__init__(self, master)
    self.logger = logging( os.path.abspath('.'), __name__ + '.ArgsCheckBar' )
    self.logger.info( '.__inti__(master=%s)' % repr(master) )

    #self.transient(master)
    #self.title('参数设定')
    #self.minsize(70, 150)
    #self.resizable(False, False)

    self.selectArgs = {
        'year': 1998, 'month': 2, 'day': 1, 'time': 0, \
        'lev': 500, 'lat': (0, 90), 'lon': (30, 180), \
        # physicial args flag
        'tt': 0, 'high': 0, 'wind': 0, 'rh': 0, \
        }

  def draw( self ):
    # draw date line

    var_year = IntVar()
    var_year.set(self.selectArgs['year'])
    Entry(self, textvariable=var_year, width=6).grid(row=0, column=0, sticky=E)
    Label(self, text='年').grid(row=0, column=1, sticky=EW)

    var_month = IntVar()
    var_month.set(self.selectArgs['month'])
    months = [i for i in range(1, 13)]
    OptionMenu(self, var_month, *months).grid(row=0, column=2, sticky=E)
    Label(self, text='月').grid(row=0, column=3, sticky=EW)

    var_day = IntVar()
    var_day.set(self.selectArgs['day'])
    Entry(self, textvariable=var_day, width=6).grid(row=1, column=0, sticky=E)
    Label(self, text='日').grid(row=1, column=1, sticky=EW)

    var_level = IntVar()
    var_level.set(self.selectArgs['lev'])
    levels = [i for i in range(200, 900, 100)]
    OptionMenu(self, var_level, *levels).grid(row=1, column=2, sticky=E)
    Label(self, text='百帕').grid(row=1, column=3, sticky=EW)

    var_time = StringVar()
    times = ['上午', '下午']
    var_time.set(times[0])
    OptionMenu(self, var_time, *times).grid(row=2, column=0, \
                                            columnspan=2, sticky=EW)
    
    var_hour = IntVar()
    var_hour.set(0)
    Entry(self, textvariable=var_hour, width=6).grid(row=2, column=2, stick=E)
    Label(self, text='时').grid(row=2, column=3, stick=EW)

    var_lon_fr = IntVar()
    var_lon_fr.set(self.selectArgs['lon'][0])
    Label(self, text='经度').grid(row=3, column=0, sticky=EW)
    Entry(
        self, textvariable=var_lon_fr, width=6
        ).grid(row=3, column=1, sticky=E)

    var_lon_to = IntVar()
    var_lon_to.set(self.selectArgs['lon'][1])
    Label(self, text='到').grid(row=3, column=2, sticky=EW)
    Entry(
        self, textvariable=var_lon_to, width=6
        ).grid(row=3, column=3, sticky=E)

    var_lat_fr = IntVar()
    var_lat_fr.set(self.selectArgs['lat'][0])
    Label(self, text='纬度').grid(row=4, column=0, sticky=EW)
    Entry(
        self, textvariable=var_lat_fr, width=6
        ).grid(row=4, column=1, sticky=E)

    var_lat_to = IntVar()
    var_lat_to.set(self.selectArgs['lat'][1])
    Label(self, text='到').grid(row=4, column=2, sticky=EW)
    Entry(
        self, textvariable=var_lat_to, width=6
        ).grid(row=4, column=3, sticky=E)

    args = ['高度', '温度', '相对湿度', '风场']
    var_args = StringVar()
    var_args.set(args[0])
    Label(
        self, text='物理量选取：'
        ).grid(row=5, column=0, columnspan=2, sticky=EW)
    OptionMenu(
        self, var_args, *args
        ).grid(row=5, column=2, columnspan=2, sticky=EW)

    singleArgs = {
        'var_year': var_year, 'var_month': var_month, \
        'var_day': var_day, 'var_level': var_level, \
        'var_time': var_time, 'var_hour': var_hour, \
        'var_lon_fr': var_lon_fr, 'var_lon_to': var_lon_to, \
        'var_lat_fr': var_lat_fr, 'var_lat_to': var_lat_to, \
        'var_args': var_args, \
        }
    self.logger.debug( 'singleArgs:\t%s' % repr(singleArgs))

    checkString = StringVar()
    checkString.set('')
    Label(
        self, textvariable=checkString,fg='red'
        ).grid(row=20, column=0, columnspan=2, sticky=EW)
    command = partial(self._ArgsCheck, singleArgs, checkString)
    Button(
        self, text='确认', command=command
        ).grid(row=20, column=2, columnspan=2, sticky=E)
    
  def _ArgsCheck( self, args, strvar ):
    self.logger.info( '._ArgsCheck(args=%s)' % repr(args) )
    
    try:
      args['var_year'].get()
      args['var_day'].get()
      args['var_hour'].get()
      args['var_lon_fr'].get()
      args['var_lon_to'].get()
      args['var_lat_fr'].get()
      args['var_lat_to'].get()
    except ValueError:
      strvar.set('参数必须为整数')
      return None

    if args['var_year'].get() < 1992:
      strvar.set('年数输入错误')
      return None

    max_dayrange = calendar.monthrange(
        args['var_year'].get(), args['var_month'].get()
        )[1]
    if args['var_day'].get() > max_dayrange:
      strvar.set('日数输入错误')
      return None

    if args['var_hour'].get() > 12 or args['var_hour'] < 0:
      strvar.set('时间输入错误')
      return None

    if args['var_lon_fr'].get() >= args['var_lon_to'].get() \
        or args['var_lon_fr'].get() < 0:
      strvar.set('经度输入错误')
      return None

    if args['var_lat_fr'].get() >= args['var_lat_to'].get() \
        or args['var_lat_fr'].get() < 0:
      strvar.set('纬度输入错误')
      return None 

    strvar.set('调用绘图')



if __name__ == '__main__':
  a = ArgsCheckBar( Tk() )
  a.draw()
  a.pack(expand=True, fill=BOTH)
  mainloop()
