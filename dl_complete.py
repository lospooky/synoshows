#! /usr/bin/env python

import time
from QueueProcessor import QueueProcessor
from Archiver import Archiver
from PbFormatter import PbFormatter
from PbNotifier import PbNotifier

processor = QueueProcessor(False)
archiver = Archiver(False)
formatter = PbFormatter()
pb = PbNotifier()

time.sleep(5)

movedItems, otherItems = processor.ProcessQueue()

if(len(movedItems) > 0):
  report = archiver.Archive(movedItems)
  title, note = formatter.FormatShowsNote(report)
  pb.NotifyNote(title, note)
  
if(len(otherItems) > 0):
  title, note = formatter.FormatDLCompleteNote(otherItems)
  pb.NotifyNote(title, note)
    