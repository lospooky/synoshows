#! /usr/bin/env python

#Utility script to sanitize Synology media/videostation built-in db
#removes db entries for which a matching file is not found on disk
#Probable issues with files with spaces/special characters in the name

import os
import subprocess

def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline,b'')
    
def quotify(self, pathname):
    pathname = '"' + pathname + '"'
    return pathname


cmd = ['/usr/syno/pgsql/bin/psql', 'mediaserver', 'admin', '-tA','-c','select path from video']
cmd1 = ['echo', 'a'] 


n = 0
for line in run_command(cmd):
    line = line.rstrip()
    #print line
    if os.path.isfile(line):
        continue
    else:
        print "Specified File Not Found, Removing: " + line
        os.system('synoindex -d' + ' ' + quotify(line))
        n = n + 1
        
print "\nRemoved " + str(n) + " files" 
