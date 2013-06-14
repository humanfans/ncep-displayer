#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import sys
import json
import pickle
import codecs
from myTools import IntStr



ans = {'blizzard': {}, 'snow': {}, 'sand': {}, 'total': {}}
# pwd = r'E:\laisky\dropbox\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer'
# pwd = r'E:\Dropbox\201211_01_NCEP-displayer'
# pwd = os.path.dirname(sys.executable)
pwd = os.path.abspath(os.getcwd())

result_file = open(os.path.join(pwd, 'historia.dat'), 'wb')
result_json = open(os.path.join(pwd, 'historia.txt'), 'w')

# <input blizzard data>
if os.path.isfile(os.path.join(pwd, 'his_blizzard.txt')):
  data_file = codecs.open(os.path.join(pwd, 'his_blizzard.txt'), 'r', 'gbk')
  data = data_file.readlines()

  for each_line in data:
    each_line = each_line.strip()
    if not each_line: continue
    date = each_line.split('\t')[0]
    climate = '&'.join(each_line.split('\t')[1: -1])
    region = each_line.split('\t')[-1]
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
    day += '\t' + '暴风雪：' + climate + '\t' + region
    print year, '年', month, '月', day

    if year not in ans['blizzard']:
      ans['blizzard'].update({year: {month: [day]}})
    elif year in ans['blizzard']:
      if month not in ans['blizzard'][year]:
        ans['blizzard'][year].update({month: [day]})
      elif month in ans['blizzard'][year]:
        ans['blizzard'][year][month].append(day)
        ans['blizzard'][year][month].sort()

    if year not in ans['total']:
      ans['total'].update({year: {month: [day.split('\t')[0]+'暴风雪']}})
    elif year in ans['total']:
      if month not in ans['total'][year]:
        ans['total'][year].update({month: [day.split('\t')[0]+'暴风雪']})
      elif month in ans['total'][year]:
        ans['total'][year][month].append(day.split('\t')[0]+'暴风雪')
        ans['total'][year][month].sort()
# </input blizzard data>

# <input snow data>
if os.path.isfile(os.path.join(pwd, 'his_snow.txt')):
  data_file = codecs.open(os.path.join(pwd, 'his_snow.txt'), 'r', 'gbk')
  data = data_file.readlines()

  for each_line in data:
    each_line = each_line.strip()
    if not each_line: continue
    date = each_line.split('\t')[0]
    climate = '&'.join(each_line.split('\t')[1: -1])
    region = each_line.split('\t')[-1]
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
    day += '\t' + climate + '\t' + region
    print year, '年', month, '月', day

    if year not in ans['snow']:
      ans['snow'].update({year: {month: [day]}})
    elif year in ans['snow']:
      if month not in ans['snow'][year]:
        ans['snow'][year].update({month: [day]})
      elif month in ans['snow'][year]:
        ans['snow'][year][month].append(day)
        ans['snow'][year][month].sort()

    if year not in ans['total']:
      ans['total'].update({year: {month: [day.split('\t')[0]+'雪灾']}})
    elif year in ans['total']:
      if month not in ans['total'][year]:
        ans['total'][year].update({month: [day.split('\t')[0]+'雪灾']})
      elif month in ans['total'][year]:
        ans['total'][year][month].append(day.split('\t')[0]+'雪灾')
        ans['total'][year][month].sort()
# </input snow data>

# <input sand data>
if os.path.isfile(os.path.join(pwd, 'his_sand.txt')):
  data_file = codecs.open(os.path.join(pwd, 'his_sand.txt'), 'r', 'gbk')
  data = data_file.readlines()

  flag = True
  while flag:
    for i, each_line in enumerate(data):
      if i == len(data) -1:
        flag = False
        break
      each_line = each_line.strip()
      if not each_line: continue
      year = each_line[: 4]
      try:
        int(year)
      except:
        data[i-1] = data[i-1].strip() + '、' + ''.join(data[i].split('\t'))
        del data[i]
        break

  for each_line in data:
    each_line = each_line.strip()
    if not each_line: continue
    date = each_line.split('\t')[0]
    region = each_line.split('\t')[1]
    region = '、'.join(region.split(' '))
    year = int(date[: 4])
    month = int(date.split('.')[1])
    day = int(date.split('.')[2])
    day = IntStr(day, 2)
    day += '日' + '\t' + '沙尘：' + region
    print year, month, day

    if year not in ans['sand']:
      ans['sand'].update({year: {month: [day]}})
    elif year in ans['sand']:
      if month not in ans['sand'][year]:
        ans['sand'][year].update({month: [day]})
      elif month in ans['sand'][year]:
        ans['sand'][year][month].append(day)
        ans['sand'][year][month].sort()

    if year not in ans['total']:
      ans['total'].update({year: {month: [day.split('\t')[0]+'沙尘']}})
    elif year in ans['total']:
      if month not in ans['total'][year]:
        ans['total'][year].update({month: [day.split('\t')[0]+'沙尘']})
      elif month in ans['total'][year]:
        ans['total'][year][month].append(day.split('\t')[0]+'沙尘')
        ans['total'][year][month].sort()
# </input sand data>


pickle.dump(ans, result_file)
result_json.write(json.dumps(ans, indent=2))

result_file.close()
result_json.close()

if __name__ == '__main__':
  raw_input('ok')