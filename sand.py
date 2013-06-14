#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import sys
import json
import codecs
import pickle
from myTools import IntStr


ans = {}
pwd = r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer'
ff = r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\his_sand.txt'
data = open(pwd+r'\historia.dat', 'rb')
ans = pickle.load(data)
data.close()





texts = codecs.open(ff, 'r', 'gbk').readlines()

for each_line in texts:
  each_line = each_line.strip()
  if not each_line: continue
  date = each_line.split('\t')[0]
  year = date[: 4]
  try: year = int(year)
  except: continue
  month = int(date.split('.')[1])
  day = int(date.split('.')[2])
  day = IntStr(day, 2)
  day += '日' + '沙尘'
  print year, month, day

  if year not in ans:
    ans.update({year: {month: [day]}})
  elif year in ans:
    if month not in ans[year]:
      ans[year].update({month: [day]})
    elif month in ans[year]:
      ans[year][month].append(day)
      ans[year][month].sort()


result_json = r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\his_json.txt'
result_dat = r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\result.dat'

open(result_json, 'w').write(json.dumps(ans, indent=2))
pickle.dump(ans, open(result_dat, 'wb'))

raw_input('Ok')