#! /usr/bin/env python

from QueueProcessor import QueueProcessor
from Archiver import Archiver
from PbFormatter import PbFormatter
from PbNotifier import PbNotifier

processor = QueueProcessor(True)
archiver = Archiver(True)
formatter = PbFormatter()
pb = PbNotifier()

movedItems, otherItems = processor.ProcessQueue()
report = archiver.Archive(movedItems)
title, note = formatter.FormatShowsNote(report)
pb.NotifyNote(title, note)