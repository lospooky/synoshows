#! /usr/bin/env python

import subprocess

listFile = '/volume1/Video/Testing/mockdb.txt'
mockDbDestination = 'volume1/Video/Testing/showRSS_inbox'

def readDbFile(filePath):
    with open(filePath) as f:
      return iter(f.readlines())
    
def MockDownloadQueue():
    queue = []
    for line in readDbFile(listFile):
      queue.append([line.rstrip(),'5', mockDbDestination])
    return iter(queue)    

#for line in MockDownloadQueue():
    #print line