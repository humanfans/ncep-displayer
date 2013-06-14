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
ff = r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\his_blizzard.txt'
data = open('historia.dat', 'rb')
ans = pickle.load(data)
data.close()





texts = codecs.open(ff, 'r', 'gbk').readlines()

for each_line in texts:
  each_line = each_line.strip()
  if not each_line: continue
  date = each_line.split('\t')[0]
  climate = '&'.join(each_line.split('\t')[1: -1])
  year = int(date[: date.index('年')])
  month = int(date[date.index('年')+1: date.index('月')])
  day = date[date.index('月')+1: ]
  if '-' in day:
    day = day[: -1]
    day_fr, day_to = day.split('-')
    day_fr = IntStr(int(day_fr), 2)
    day_to = IntStr(int(day_to), 2)
    day = day_fr + '-' + day_to + '日'
  else:
    day = day[: -1]
    day = IntStr(int(day), 2)
    day += '日'
  day += '暴风雪' + climate
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