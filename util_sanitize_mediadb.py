#! /usr/bin/env python

import os
import subprocess

def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline,b'')


cmd = ['/usr/syno/pgsql/bin/psql', 'mediaserver', 'admin', '-tA','-c','select path from video']
cmd1 = ['echo', 'a'] 


n = 0
for line in run_command(cmd):
    line = line.rstrip()
    #print line
    if os.path.isfile(line):
        continue
    else:
        print line
        os.system('synoindex -d' + ' ' + line)
        n = n + 1
        
print n 
