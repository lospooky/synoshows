#! /usr/bin/env python

import subprocess

queryString = ['/usr/syno/pgsql/bin/psql', 'download', 'admin', '-tA','-c','select filename, status, destination from download_queue']
clearQueueString = ['/usr/syno/pgsql/bin/psql', 'download', 'admin', '-c', 'DELETE from download_queue WHERE status = 5']

def dbQuery(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline,b'')
    
def DownloadStationQueue():
    queue = []
    for line in dbQuery(queryString):
      queue.append(line.rstrip().split("|"))
    return iter(queue)
    
def ClearDownloadQueue():
  dbQuery(clearQueueString)
  #output = []
  #for line in dbQuery(clearQueueString):
    #output.append(line)
  #return iter(output)

#for line in DownloadStationQueue():
    #print line
    
#ClearDownloadQueue()