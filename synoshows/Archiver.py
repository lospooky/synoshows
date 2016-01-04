#! /usr/bin/env python

import os
import shutil
import subprocess

class Archiver:
    def __init__ (self, isTest):
      self.isTest = isTest
      self.commandString = ['tvnamer', '{file}', '--config' ,'/volume1/Software/Synology/tvnamerconfig.json']
      if(self.isTest == False):
        self.archivePath = '/volume1/Video/Shows/'
      else:
        self.archivePath = '/volume1/Video/Testing/Shows/'

    def tvnamer_invoke(self, fileName):
      command = list(self.commandString)
      command[1] = fileName
      print command
      p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      return iter(p.stdout.readline,b'')

    def fix_americandad(self, oldpath):
      #Fix filename
      epid = os.path.basename(oldpath).split(' - ', 2)[1]
      seasonNumber = int(epid.split('x')[0])
      fixedepid = epid.replace(epid.split('x')[0], str(seasonNumber+1), 1)
      newpath = oldpath.replace(epid, fixedepid, 1)
      os.rename(oldpath, newpath)

      #ReInvokes tvnamer
      for line in self.tvnamer_invoke(newpath):
        if line.startswith('New path: '):
          return line.rstrip().lstrip('New path: ')

    def tvnamer_postprocessing(self, outputstring):
        newfullpath = outputstring.rstrip().lstrip('New path: ')
        if "American Dad!" in newfullpath:
          newfullpath =  self.fix_americandad(newfullpath)
        newfilename = os.path.basename(newfullpath)
        splits = newfilename.split(' - ', 2)
        showName = splits[0].replace('!', '').rstrip('.')
        showSeason = splits[1].split('x',1)[0]
        return [newfullpath, showName, showSeason]

    def movetoArchive(self, filespec):
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
        #print(f)
        #American Dad Skipping Fix
        if "American" in f:
          report.append(['KO', f])
          #report.append(['KO', os.path.basename(line.rstrip().lstrip('Skipping file: '))])
          continue
        for line in self.tvnamer_invoke(f):
          print line
          if line.startswith('New path:'):
            renamedItem = self.tvnamer_postprocessing(line)
            self.movetoArchive(renamedItem)
            report.append(['OK', os.path.basename(renamedItem[0])])
          elif line.startswith('Skipping file:'):
            report.append(['KO', os.path.basename(line.rstrip().lstrip('Skipping file: '))])
      return report