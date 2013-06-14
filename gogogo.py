#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import sys
from libs import makegs

aa = makegs.Make(
    gsFilePath=r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\test.gs', \
    dataFilePath=r'X:\pressure\air.1998.nc', \
    resultPath=r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\res', \
    gradsExecPath = r'X:\GrADS19\win32\grads.exe'
    )

print '创建.gs文件...'.encode('gbk')
print aa.MakeFile()

print '摁回车开始绘图'.encode('gbk')
raw_input('')
print aa.Draw()

raw_input('完成'.encode('gbk'))
