#! /usr/bin/env python

import os
import shutil

#Reads master file with mock show names and path and generates them at dlPath

def GenerateTestFiles(dlPath, mockDbFile):
  #Clears anything within dlPath
  for root, dirs, files in os.walk(dlPath):
    for f in files:
    	os.unlink(os.path.join(root, f))
    for d in dirs:
    	shutil.rmtree(os.path.join(root, d))
  
  with open(mockDbFile) as f:
    for line in f:
      fullmockfilename = os.path.join(dlPath, line.rstrip())
      mockbasepath = os.path.dirname(fullmockfilename)
      if not os.path.exists(mockbasepath):
        os.makedirs(mockbasepath)
      #print "Generating: " + fullmockfilename
      open(fullmockfilename, 'w+').close()                     