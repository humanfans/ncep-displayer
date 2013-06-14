#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import os
import sys
import pickle
import json

pwd = os.path.abspath(os.getcwd())
files = os.walk(pwd).next()[2]
output = {}

for each_file in files:
  ans = ''
  script = open(os.path.join(pwd, each_file), 'r').readlines()

  length = len(script)
  for i in range(length-1, -1, -1):
    if 'printim' in script[i]:
      end_line = i
    if 'q dim' in script[i]:
      start_line = i
      # break
  ans = ''.join(script[start_line+1: end_line])
  cate = os.path.splitext(each_file)[0]
  output.update({cate: ans})

# file_name = os.path.splitext(each_file)[0] + ".dat"
file_name = "single.dat"
new_file = open(file_name, 'wb')
pickle.dump(output, new_file)
new_file.close()

# <debug json view>
json_file = "json.txt"
json_file = open(json_file, 'w')
json_file.write(json.dumps(output, indent=4))
json_file.close()
# </debug json view>