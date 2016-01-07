#! /usr/bin/env python

def readDbFile(filePath):
    with open(filePath) as f:
      return iter(f.readlines())
    
def MockDownloadQueue(mockDbFile, pathAsInDb):
    queue = []
    for line in readDbFile(mockDbFile):
      queue.append([line.rstrip(),'5', pathAsInDb])
      #print [line.rstrip(),'5', pathAsInDb]
    return iter(queue)    