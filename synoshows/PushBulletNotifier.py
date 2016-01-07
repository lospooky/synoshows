#! /usr/bin/env python

from pushbullet import PushBullet

class PushBulletNotifier:
  def __init__ (self, pb_apikey):
    #Write your PushBullet API Key Here
    self.pb_apikey = pb_apikey
    self.pb = PushBullet(self.pb_apikey)
    self.notifiedDevices = filter(deviceFilter, self.pb.devices)
    #print self.pb.devices
    return
    
  def NotifyNote(self, title, string):
    for d in self.notifiedDevices:
      d.push_note(title, string)
    #Alternative to push directly to all PushBullet devices:
    #self.pb.push_note(title, string)
    return
      
def deviceFilter(x):
  #Configures the devices to push the notification to
  #For more information:
  #https://docs.pushbullet.com/#list-devices
  #https://github.com/randomchars/pushbullet.py
  #Example: for pushing only to your Nexus 5 phone 
  #return x.manufacturer == "LGE" and x.model == "Nexus 5"
  #Default x: push to all devices
  return x