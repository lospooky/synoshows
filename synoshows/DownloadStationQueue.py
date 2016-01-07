#! /usr/bin/env python

#Accesses the Synology DownloadStation queue via the built-in PostgreSQL db

import subprocess

queryString = ['/usr/syno/pgsql/bin/psql', 'download', 'admin', '-tA','-c','select filename, status, destination from download_queue']
clearQueueString = ['/usr/syno/pgsql/bin/psql', 'download', 'admin', '-c', 'DELETE from download_queue WHERE status = 5']

def dbQuery(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline,b'')

#Returns and structures information in the download queue    
def DownloadStationQueue():
    queue = []
    for line in dbQuery(queryString):
      queue.append(line.rstrip().split("|"))
    return iter(queue)

#Clears completed download items, status == 5    
def ClearDownloadQueue():
  dbQuery(clearQueueString)