#! /usr/bin/env python

# Use it to check if DownloadStation/Transmission download completed script is correctly triggered
#Each time a download completes, it will create/append a line to the fname file
fname = '/volume1/Downloads/scriptdebug.txt'
with open(fname, 'a') as f:
    f.write('DL Complete!\n')