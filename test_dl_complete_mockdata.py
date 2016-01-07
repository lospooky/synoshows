#! /usr/bin/env python

#Generates mock files + downloadstation queue and runs the scripts on them

from synoshows import SettingsLoader
from synoshows import QueueProcessor
from synoshows import Archiver
from synoshows import NoteFormatter
from synoshows import PushBulletNotifier

settings = SettingsLoader.LoadSettings()

test = True
configuration = settings["test"]

processor = QueueProcessor(test, configuration)
archiver = Archiver(test, configuration["archivePath"], settings["tvnamerconfig_path"])
formatter = NoteFormatter()
pb = PushBulletNotifier(settings["pushbulletkey"])

movedItems, otherItems = processor.ProcessQueue()
report = archiver.Archive(movedItems)
title, note = formatter.FormatShowsNote(report)
pb.NotifyNote(title, note)