#! /usr/bin/env python
# -*- coding: utf-8



from __future__ import unicode_literals
from Tkinter import *
import os
import sys
import datetime
import codecs
import pickle
from myTools import PathSwitch
from myTools import MyException
from myTools import IntStr
from myTools import logging

# <Debug>
# root = Tk()
# pwd = sys.path[0]
# </Debug>

class makegsError( MyException ):
  def __init__( self, num, text='' ):
    MyException.__init__( self, num, text )


class Makegs():

  def __init__(
      self,
      gsFilePath=None, dataDocPath=None,
      imagePath=None, gradsExecPath=None,
      lat = (0, 90), lon = (30, 180),
      lev = 500,
      timeRange = ( datetime.datetime( 1998, 3, 1, 0, 0, 0 ),
                    datetime.datetime( 1998, 3, 1, 0, 0, 0 ) ),
      ):
    """
    make a .gs file
    """

    self.logger = logging(
        os.path.abspath(os.getcwd()), __name__ + '.Make',
        # disabled=True
        )

    self.logger.info(
        '.__init__(gsFilePath=%s, dataDocPath=%s, '
        'imagePath=%s, gradsExecPath=%s, '
        'lat=%s, lon=%s, '
        'lev=%s, '
        'timeRange=%s'
        % (repr(gsFilePath), repr(dataDocPath),
           repr(imagePath), repr(gradsExecPath),
           repr(lat), repr(lon), repr(lev),
           repr(timeRange))
        )
    if gsFilePath:
      gs_file_path = PathSwitch( gsFilePath )
    else: gs_file_path = None
    if dataDocPath:
      data_file_path = PathSwitch( dataDocPath )
    else: data_file_path = None
    if imagePath:
      image_path = PathSwitch( imagePath )
    else: image_path = None

    if data_file_path:
      if not os.path.isfile( data_file_path ):
        self.logger.error( '001: data_file_path: %s' % repr( data_file_path ) )
        raise makegsError( 001, 'data_file_path: %s' % repr( data_file_path ) )

    if gs_file_path:
      gs_doc_path = os.path.split( gs_file_path )[0]
      if not os.path.exists( gs_doc_path ):
        self.logger.error( '002: gs_file_path: %s' % repr( gs_doc_path ) )
        raise makegsError( 002, 'gs_file_path: %s' % repr( gs_doc_path ) )

    if image_path:
      if not os.path.isdir( os.path.dirname(image_path) ):
        self.logger.error( '004: image_path: %s' % repr( image_path ) )
        raise makegsError( 004, 'image_path: %s' % repr( image_path ) )

    if gradsExecPath:
      if not os.path.isfile( gradsExecPath ):
        self.logger.error( '005: gradsExecPath: %s' % repr( gradsExecPath ) )
        raise makegsError( 005, 'gradsExecPath: %s' % repr( gradsExecPath ) )

    time_range = ['', '']
    time_range[0] = self.Datatime2Grads( timeRange[0] )
    time_range[1] = self.Datatime2Grads( timeRange[1] )

    self.parameter = {
        'gs_file_path': gs_file_path,
        'data_file_path': data_file_path,
        'lat': lat, 'lon': lon,
        'lev': lev,
        'time_range': time_range,
        'image_path': imagePath,
        'grads_path': gradsExecPath,
        'whether_cint': True,
        'title': '',
        'whether_multi': False,
        'single_arg': '',
        'multi_arg': '',
        'date_time': ['', '', '', ''],
        }

  def config_NCEP( self, dataStream ):
    """
    support to NCEPDisplayer dataStream
    """
    self.logger.info( '._ArgsConfig(dataStream=%s)' % repr(dataStream) )

    self.dataStream = dataStream

    par = self.parameter
    data = dataStream

    the_year = data['phyArgs']['year'][0]
    the_month = data['phyArgs']['month'][0]
    the_day = data['phyArgs']['day'][0]
    the_time = int(data['phyArgs']['time'][0])
    the_timeRange = datetime.datetime(
        the_year, the_month, the_day, the_time
        )
    the_timeRange = self.Datatime2Grads( the_timeRange )

    par['gs_file_path'] = data['sysArgs']['gsFilePath']
    par['data_file_path'] = data['sysArgs']['gsDataPath']
    par['grads_path'] = data['sysArgs']['gsExecPath']
    par['lat'] = (data['phyArgs']['lat_fr'][0], data['phyArgs']['lat_to'][0])
    par['lon'] = (data['phyArgs']['lon_fr'][0], data['phyArgs']['lon_to'][0])
    par['lev'] = dataStream['phyArgs']['high'][0]
    par['date_time'] = [the_year, the_month, the_day, the_time]
    par['time_range'] = (the_timeRange, the_timeRange)
    par['image_path'] = os.path.join(
        data['sysArgs']['gsDocPath'], data['posterStatus']['img_name']
        )
    par['whether_multi'] = not data['phyArgs']['whether_custom'][0]
    par['single_arg'] = data['phyArgs']['args'][0].get()
    par['multi_arg'] = data['phyArgs']['multi'][0]

  def _ArgSwitch( self, the_arg, ground=False ):
    """
    switch the args from dataStream to ncep's nc data
    """
    self.logger.info( '._ArgSwitch()' )

    par = self.parameter
    data = self.dataStream

    if not ground:
      the_dict = {
          '温度': 'air',
          '高度': 'hgt',
          '相对湿度': 'rhum',
          '风场': 'uv',
          '绝对湿度': 'shum',
          # multi_arg
          '500 高度 & 850h uv & rh': 'uvrhumhgt',
          '700 风场 & 700 相对湿度': 'uvrhum.700',
          '850 风场 & 850 相对湿度': 'uvrhum.850',
          '500 高度 & 850 温度': 'hgt_air',
          }
    elif ground:
      the_dict = {
          '温度': 'air.2m.gauss',
          '高度': 'hgt',
          '相对湿度': 'rhum.sig995',
          '地面气压': 'pres.sfc.gauss',
          '抬升指数': 'lftx.sfc',
          '水汽含量': 'pr_wtr.eatm',
          '海平面气压': 'slp',
          }

    if the_arg not in the_dict:
      self.logger.error( '008 Not Defined the_arg: %s' % repr(the_arg) )
      raise makegsError( 8, 'Not Defined the_arg: %s' % repr(the_arg) )

    self.logger.info( '_ArgSwitch return: %s' % repr(the_dict[the_arg]) )
    return the_dict[the_arg]

  def _SdfOpen( self ):
    """
    create the sentence of GrADs' sdfopen sentence
    """
    self.logger.info( '._SdfOpen()' )

    par = self.parameter
    pre_ans = "'sdfopen %s" % par['data_file_path']
    the_ans = ''

    # <single argument images>
    if not par['whether_multi']:
      the_arg = par['single_arg']
      if par['lev'] != '地面':
        nc_arg = self._ArgSwitch( the_arg, ground=False )
      else:
        nc_arg = self._ArgSwitch( the_arg, ground=True )

      if par['lev'] != '地面':
        if nc_arg == 'uv':
          the_ans = os.path.join(
              pre_ans, 'pressure', "uwnd.%s.nc '\n" % par['date_time'][0]
              )
          the_ans += os.path.join(
              pre_ans, 'pressure', "vwnd.%s.nc '\n" % par['date_time'][0]
              )
        else:
          the_ans = os.path.join(
              pre_ans, 'pressure',
              "%s.%s.nc '\n" % (nc_arg, par['date_time'][0])
              )

      elif par['lev'] == '地面':
        if nc_arg == 'uv.10m':
          the_ans = os.path.join(
              pre_ans, "pressure", "uwnd.10m.gauss.%s.nc' \n"
              % par['date_time'][0]
              )
          the_ans = os.path.join(
              pre_ans, "pressure", "vwnd.10m.gauss.%s.nc' \n"
              % par['date_time'][0]
              )
        else:
          the_ans = os.path.join(
              pre_ans, "pressure", "%s.%s.nc' \n"
              % (nc_arg, par['date_time'][0])
              )
    # </single argument images>

    # <multi_arg images>
    elif par['whether_multi']:
      the_arg = par['multi_arg'].strip()

      if the_arg == '500 高度 & 850h uv & rh':
        the_ans = os.path.join(
            pre_ans, "pressure", "uwnd.%s.nc' \n"
            % (par['date_time'][0])
            )
        the_ans += os.path.join(
            pre_ans, "pressure", "vwnd.%s.nc' \n"
            % (par['date_time'][0])
            )
        the_ans += os.path.join(
            pre_ans, "pressure", "rhum.%s.nc' \n"
            % (par['date_time'][0])
            )
        the_ans += os.path.join(
            pre_ans, "pressure", "hgt.%s.nc' \n"
            % (par['date_time'][0])
            )

      elif (the_arg == '700 风场 & 700 相对湿度'
            or the_arg == '850 风场 & 850 相对湿度'):
        the_ans = os.path.join(
            pre_ans, "pressure", "uwnd.%s.nc' \n"
            % (par['date_time'][0])
            )
        the_ans += os.path.join(
            pre_ans, "pressure", "vwnd.%s.nc' \n"
            % (par['date_time'][0])
            )
        the_ans += os.path.join(
            pre_ans, "pressure", "rhum.%s.nc' \n"
            % (par['date_time'][0])
            )

      elif the_arg == '500 高度 & 850 温度':
        the_ans = os.path.join(
            pre_ans, "pressure", "hgt.%s.nc' \n"
            % (par['date_time'][0])
            )
        the_ans += os.path.join(
            pre_ans, "pressure", "air.%s.nc' \n"
            % (par['date_time'][0])
            )
    # </multi_arg images>


    self.logger.info( '_SdfOpen return: %s' % repr(the_ans) )
    return the_ans

  def Datatime2Grads( self, the_datatime ):
    """
    the_datatime is a datatime.datetime instance
    swith the time's format to GrADs from datetime.datetime
    """
    self.logger.info( '.Datatime2Grads(the_datatime=%s' % repr(the_datatime) )

    if not isinstance (the_datatime, datetime.datetime):
      raise makegsError( 003, 'time_range: %s' % repr( the_datatime ) )
    hour = IntStr( the_datatime.hour, 2 )
    day = IntStr( the_datatime.day, 2 )
    month = the_datatime.strftime( '%b' ).upper()
    year = IntStr( the_datatime.year, 4 )

    self.logger.info(
        'Datatime2Grads return: %s'
        % repr(hour + 'Z' + day + month + year)
         )
    return hour + 'Z' + day + month + year

  def _Script( self ):
    """
    return the .gs script's texts
    """
    self.logger.info( '_Script()' )

    par = self.parameter
    data = self.dataStream

    # <single image>
    script_name = "single.dat"
    if not par['whether_multi']:
      the_arg = par['single_arg']
      if par['lev'] != '地面':
        nc_arg = self._ArgSwitch( the_arg, ground=False )
      else:
        nc_arg = self._ArgSwitch( the_arg, ground=True )

    elif par['whether_multi']:
      nc_arg = self._ArgSwitch( par['multi_arg'].strip() )

    script_path = os.path.join(
        data['sysArgs']['hostPath'], 'scripts', script_name
        )
    script_path = PathSwitch( script_path )
    # </single image>

    if not os.path.isfile(script_path):
      self.logger.error( '009 NotFound gs script: %s' % repr(script_path) )
      raise makegsError( 9, 'NotFound gs script: %s' % repr(script_path) )

    try:
      with open(script_path, 'rb') as script_file:
        the_texts = pickle.load(script_file)
        the_texts = the_texts[nc_arg]
    except Exception, e:
      self.logger.error(
          "010:script file: %s, error: %s" % (script_path, repr(e))
          )
      raise makegsError( 10, "script file: %s" % script_path )

    self.logger.info( '_Script return: %s' % repr(the_texts) )
    return the_texts

  def makefile( self ):
    """
    create a .gs file
    """
    self.logger.info( '.makefile()' )

    par = self.parameter

    gs_file = open(par['gs_file_path'], 'w')

    gs_file.write("'reinit'\n")
    gs_file.write(self._SdfOpen())
    gs_file.write("'set mpdset cnworld cnriver'\n")
    gs_file.write("'set map 15 1 3'\n")
    gs_file.write("'set lat %s %s'\n" % (par['lat'][0], par['lat'][1]))
    gs_file.write("'set lon %s %s'\n" % (par['lon'][0], par['lon'][1]))
    if par['lev'] != '地面':
      gs_file.write("'set lev %s'\n" % par['lev'])
    gs_file.write("'set time %s '\n" % (par['time_range'][0]))
    gs_file.write(self._Script())
    gs_file.write(
        "\n'printim %s gif x1024 y768 white' \n"
        % par['image_path']
        )
    gs_file.write(";\n")
    gs_file.write("quit \n")

    gs_file.close()

    return par['gs_file_path']

  def draw( self ):
    """
    draw the pictures depend on the .gs file
    """
    self.logger.info( '.draw()' )
    par = self.parameter

    if os.path.isfile(par['image_path']):
      return par['image_path']

    try:
      os.system( "%s -bcl %s" % ( par['grads_path'], par['gs_file_path'] ) )
    except Exception, e:
      raise makegsError( 006, 'Make.DrawError: %s' % repr( e ) )

    if not os.path.isfile(par['image_path']): return None
    self.logger.info( 'draw return:%s' % repr(par['image_path']) )
    return par['image_path']

# -------------------------------------------------
if __name__ == '__main__':
  dataStream = {
      'phyArgs': {
          'year': [1998, IntVar()], 'month': [2, IntVar()],
          'day': [1, IntVar()], 'time': [0, IntVar()],
          'high': ['500 ', StringVar()],
          'lon_fr': [30, IntVar()], 'lon_to': [180, IntVar()],
          'lat_fr': [0, IntVar()], 'lat_to': [90, IntVar()],
          'historia': ['刷新', StringVar()],
          'multi': ['500 高度 & 850h uv & rh', StringVar()],
          'args': [StringVar(), [['height', 'tt', 'rh', 'wind'],
                                ['500 高度 & 850h uv & rh',
                                 '700 风场 & 700 相对湿度',
                                 '850 风场 & 850 相对湿度',
                                 '500 高度 & 850 温度    ']]],
          'whether_historia': [0, IntVar()],
          'whether_custom': [1, IntVar()],
          },
      'sysArgs': {
          'hostPath': pwd,
          'gsFilePath': os.path.join(pwd, 'gsfile.gs'),
          'gsExecPath': r'X:\GrADS19\win32\grads.exe',
          'gsDataPath': 'X:\\',
          'gsDocPath': os.path.join(pwd, 'images'),
          },
      'posterStatus': {
          'posterAlbum': {'main': ['', '']},
          'hintInfo': ['', StringVar()],
          'img_name': 'test.gif',
          },
      }

  dataStream['phyArgs']['args'][0].set('温度')

  makegs = Makegs()
  makegs.config_NCEP( dataStream )
  makegs.makefile()
  makegs.draw()