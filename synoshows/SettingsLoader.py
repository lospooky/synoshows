#! /usr/bin/env python

import json

def LoadSettings():
  settings = json.loads(open('settings.json').read())
  return settings