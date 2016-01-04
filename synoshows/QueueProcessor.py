#! /usr/bin/env python

import os
import fnmatch
import shutil

from GenerateTestFiles import GenerateTestFiles
from MockDownloadQueue import MockDownloadQueue
from DownloadStationQueue import DownloadStationQueue
from DownloadStationQueue import ClearDownloadQueue

class QueueProcessor:
  def __init__(self, isTest):
      self.isTest = isTest
      if(self.isTest == False):
        self.filetypes = ['*.avi', '*.mkv', '*.mp4', '*.wmv']
        self.dbDlPath = 'Downloads/showRSS_inbox'
        self.dlPath = '/volume1/Downloads/showRSS_inbox/'
        self.dstPath = '/volume1/Video/Inbox/'
      else:
        self.filetypes = ['*.txt']
        self.dbDlPath = 'volume1/Video/Testing/showRSS_inbox'
        self.dlPath = '/volume1/Video/Testing/showRSS_inbox/'
        self.dstPath = '/volume1/Video/Testing/Inbox/'   

  def DownloadQueueData(self):
    if (self.isTest==False):
        return DownloadStationQueue()
    else:
        GenerateTestFiles()
        return MockDownloadQueue()

  def DirectoryParser(self,srcPath):
    for dirname, subdirs, files in os.walk(srcPath):
        for file in files:
            for ftype in self.filetypes:
                if fnmatch.fnmatch(file, ftype) and not "sample" in file:
                    return ([os.path.join(dirname,file), os.path.join(self.dstPath, file)])
    return

  def CleanUp(self):
    os.chdir(self.dlPath)
    for root, dirs, files in os.walk('.'):
      #for f in files:
        #os.unlink(os.path.join(root,f))
      for d in dirs:
        shutil.rmtree(os.path.join(root, d))
    
    if(self.isTest == False):
      ClearDownloadQueue()
      
    


  def ProcessQueue(self):
      moveList = []
      otherList = []
      #Parse Queue
      for line in self.DownloadQueueData():
        #print line
        if (line[1] == "5" and line[2] == self.dbDlPath):
            itemPath = os.path.join(self.dlPath, line[0])
            #It's a File
            if(os.path.isfile(itemPath)):
              moveList.append([itemPath, os.path.join(self.dstPath, line[0])])
            #It's a Directory
            elif(os.path.isdir(itemPath)):
              itemInDir = self.DirectoryParser(itemPath)
              moveList.append(itemInDir)
        #NON SHOWRSS DOWNLOADED ITEMS
        if (line[1] == "5" and line[2] != self.dbDlPath):
            itemPath = os.path.join("/volume1", os.path.join(line[2], line[0]))
            #print(os.path.exists(itemPath))
            if (os.path.exists(itemPath)):
              otherList.append(line[0])

      #Move items, CleanUp, Return relevant items path
     #print moveList 
      for item in moveList:
        #print item[0]
        #print item[1]
        shutil.move(item[0], item[1])
        #print item[0]
      self.CleanUp()

      
      return [map(lambda x:x[1], moveList), otherList]

#processor = QueueProcessor(True)
#movedItems = processor.ProcessQueue()
#print movedItems