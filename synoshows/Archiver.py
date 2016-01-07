#! /usr/bin/env python

#Invokes tvnamer and renames show files
#Moves them from the folder they've been downloaded to, to your library archive path
#Adds them to the Synology media index/videostation database
#Outputs information to setup PushBullet Notifications

import os
import shutil
import subprocess

class Archiver:
    def __init__ (self, isTest, archivePath, tvnamerconfig_path):
      self.isTest = isTest
      self.commandString = ['tvnamer', '{file}', '--config' , tvnamerconfig_path]
      self.archivePath = archivePath

    #Invokes tvnamer, reads output from stdout
    def tvnamer_invoke(self, fileName):
      command = list(self.commandString)
      command[1] = fileName
      #print command
      p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      return iter(p.stdout.readline,b'')

    #Extracts relevant information from tvnamer output
    def tvnamer_postprocessing(self, outputstring):
        newfullpath = outputstring.rstrip().lstrip('New path: ')
        newfilename = os.path.basename(newfullpath)
        splits = newfilename.split(' - ', 2)
        showName = splits[0].replace('!', '').rstrip('.')
        showSeason = splits[1].split('x',1)[0]
        return [newfullpath, showName, showSeason]

    #Moves file from download directory to archive directory
    def movetoArchive(self, filespec):
        #File will be archived in archivePath/Show Name/Season X/episodefilename
        dstDir = self.archivePath + filespec[1] + '/Season ' + filespec[2] + '/'
        if not os.path.isdir(dstDir):
          os.makedirs(dstDir)
          os.chmod(dstDir,0o777)
          os.chmod(self.archivePath+filespec[1]+'/', 0o777)
        archivedfullpath = os.path.join(dstDir, os.path.basename(filespec[0]))
        shutil.move(filespec[0], archivedfullpath)
        os.chmod(archivedfullpath, 0o777)
        #Adds file to synology media index
        if(self.isTest == False):
            os.system('synoindex -a' + ' ' + self.quotify(archivedfullpath))

    def quotify(self, pathname):
      pathname = '"' + pathname + '"'
      return pathname

    def Archive(self, inboxfiles):
      report = []
      #print inboxfiles
      for f in inboxfiles:
        for line in self.tvnamer_invoke(f):
          #print line
          #Produces a report to set up PushBullet Notification Text
          if line.startswith('New path:'):
            renamedItem = self.tvnamer_postprocessing(line)
            self.movetoArchive(renamedItem)
            report.append(['OK', os.path.basename(renamedItem[0])])
          elif line.startswith('Skipping file:'):
            report.append(['KO', os.path.basename(line.rstrip().lstrip('Skipping file: '))])
      return report