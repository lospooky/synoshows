#! /usr/bin/env python

import time
from synoshows import SettingsLoader
from synoshows import QueueProcessor
from synoshows import Archiver
from synoshows import NoteFormatter
from synoshows import PushBulletNotifier

settings = SettingsLoader.LoadSettings()

test = False
configuration = settings["live"]

processor = QueueProcessor(test, configuration)
archiver = Archiver(test, configuration["archivePath"], settings["tvnamerconfig_path"])
formatter = NoteFormatter()
pb = PushBulletNotifier(settings["pushbulletkey"])

time.sleep(5)

tvItems, otherItems = processor.ProcessQueue()

#Tv Shows Notifications
if(len(tvItems) > 0):
  report = archiver.Archive(tvItems)
  title, note = formatter.FormatShowsNote(report)
  pb.NotifyNote(title, note)

#Other Downloads Notifications  
if(len(otherItems) > 0):
  title, note = formatter.FormatDLCompleteNote(otherItems)
  pb.NotifyNote(title, note)    