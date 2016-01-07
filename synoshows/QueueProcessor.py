#! /usr/bin/env python

#Scans actual/mock DownloadStation Queue
#Moves show files to a single, unified destination path
#Cleans up shows original download path
#Monitors also non-show completed downloads
#Clears DownloadStation queue
#Returns shows destination path and other downloads original path 

import os
import fnmatch
import shutil

from GenerateTestFiles import GenerateTestFiles
from MockDownloadQueue import MockDownloadQueue
from DownloadStationQueue import DownloadStationQueue
from DownloadStationQueue import ClearDownloadQueue

class QueueProcessor:
  def __init__(self, isTest, config):
      self.isTest = isTest
      self.config = config
   
  def DownloadQueueData(self):
    if (self.isTest==False):
        #Looks up the actual DownloadStation Queue
        return DownloadStationQueue()
    else:
        #Testing, Generates mock files and DownloadStation queue
        GenerateTestFiles(self.config["downloadPath"], self.config["mockDbFile"])
        return MockDownloadQueue(self.config["mockDbFile"], self.config["pathAsInDb"])

  def DirectoryParser(self,srcPath):
    for dirname, subdirs, files in os.walk(srcPath):
        for file in files:
            for ftype in self.config["filetypes"]:
                if fnmatch.fnmatch(file, ftype) and not "sample" in file:
                    return ([os.path.join(dirname,os.path.basename(file)), os.path.join(self.config["destinationPath"], file)])
    return

  #Cleans up download path
  def CleanUp(self):
    os.chdir(self.config["downloadPath"])
    for root, dirs, files in os.walk('.'):
      for d in dirs:
        shutil.rmtree(os.path.join(root, d))
    
    #Clears completed downloadstation items
    if(self.isTest == False):
      ClearDownloadQueue()
  
  #Processes the DownloadStation Queue    
  def ProcessQueue(self):
      #Shows will be put in movelist, other completed downloads in otherlist
      moveList = []
      otherList = []
      #Parse Queue
      for line in self.DownloadQueueData():
        #print line
        #Status == 5, Is a Completed Download
        #Is a ShowRSS item, is in your main show download directory
        if (line[1] == "5" and line[2] == self.config["pathAsInDb"]):
            itemPath = os.path.join(self.config["downloadPath"], line[0])
            #It's a File
            if(os.path.isfile(itemPath)):
              moveList.append([itemPath, os.path.join(self.config["destinationPath"], os.path.basename(line[0]))])
            #It's a Directory, look into it and search for video files
            elif(os.path.isdir(itemPath)):
              itemInDir = self.DirectoryParser(itemPath)
              moveList.append(itemInDir)
        #Other Completed Downloaded Items
        if (line[1] == "5" and line[2] != self.config["pathAsInDb"]):
            itemPath = os.path.join("/volume1", os.path.join(line[2], line[0]))
            if (os.path.exists(itemPath)):
              otherList.append(line[0])

     #Moves show items to destination path, show download path cleanup, returns show destination paths and other items download path
     #print moveList 
      for item in moveList:
        #print "Source: " + item[0]
        #print "Destination: " + item[1]
        shutil.move(item[0], item[1])
      self.CleanUp()

      
      return [map(lambda x:x[1], moveList), otherList]