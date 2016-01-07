#! /usr/bin/env python

from synoshows import PushBulletNotifier

pb = PushBulletNotifier()
pb.NotifyNote("Title", "This is a note message, Yo!\nWith Two Lines, Yo!")
