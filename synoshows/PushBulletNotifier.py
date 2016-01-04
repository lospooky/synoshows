#! /usr/bin/env python

from pushbullet import PushBullet

class PushBulletNotifier:
  def __init__ (self):
    self.pbapikey = "v1fn5dViDswvPrtvE31ZLkPBQubMVNt7kyujxIRFdS4om" 
    self.pb = PushBullet(pbapikey)
    self.notifiedDevices = filter(deviceFilter, self.pb.devices)
    
  def NotifyNote(self, title, string):
    #print(self.notifiedDevices)
    #for d in self.notifiedDevices:
      #success, push = d.push_note(title, string)
    self.pb.push_note(title, string)
  
  def NotifyList(self, title, list):
     for d in self.notifiedDevices:
      success, push = d.push_list(title, list) 
    
def deviceFilter(x): return x.manufacturer == "LGE" and x.model == "Nexus 5"