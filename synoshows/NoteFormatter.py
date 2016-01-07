#! /usr/bin/env python

#Formats the PushBullet Notifications
class NoteFormatter:
    def __init__(self):
      #Note Titles and Boilerplates
      self.tvNoteTitle = "New TV Show!"
      self.dlNoteTitle = "Download Complete!"
      self.okHeader = "The following show has been successfully added to the library: \n\n"
      self.koHeader = "\nProblems encountered when archiving: \n\n" 
    
    #Tv Show Note
    def FormatShowsNote(self, archiverReport):
      successes = "\n"
      fails = ""
      for item in archiverReport:
        if item[0] is "OK":
          successes = successes + "- {show} \n".format(show=item[1])
        if item[0] is "KO":
          if fails is "":
            fails = self.koHeader
          fails = fails + "- {show} \n".format(show=item[1])  
      return [self.tvNoteTitle, successes + "\n" + fails]
    
    #Generic Download Note  
    def FormatDownloadNote(self, items):
      dlist = "\n"
      for item in items:
        dlist = dlist + "- {dl} \n".format(dl=item)
      return [self.dlNoteTitle, dlist]
      
      
    
          