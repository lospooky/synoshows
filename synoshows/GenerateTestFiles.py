#! /usr/bin/env python

import os
import shutil

srcPath = '/volume1/Video/Testing/master/'
dstPath = '/volume1/Video/Testing/showRSS_inbox/'
mockDbFilePath = '/volume1/Video/Testing/mockdb.txt'

def GenerateTestFiles():
  #shutil.rmtree(dstPath)
  if os.path.isfile(mockDbFilePath):
    os.remove(mockDbFilePath)
  
  with open(mockDbFilePath, 'a') as f:  
    for item in os.listdir(srcPath):
        #print item

        s = os.path.join(srcPath, item)
        d = os.path.join(dstPath, item)
        #print s
        #print d
        if os.path.isdir(s):
            #print "Copytree"
            shutil.copytree(s, d)
            f.write(item+'\n')
        else:
            #print "Copy2"
            shutil.copy2(s, d)
            f.write(item+'\n')
            
#GenerateTestFiles()            