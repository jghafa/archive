#!/usr/bin/python3
'''
test subprocess
'''
import subprocess

# the next line hides the output from the bash script.  PIPE displays it.
#        stdout=subprocess.DEVNULL)

# cwd sets the working directory of the bash command

# Convert is ImageMagick - it's extract single page TIFFs from a multi-page TIF
# then the bash scriptlet zips the TIFs together
#
# The string "%03d is a printf string - ImageMagick subs it for the page number
bashCmd = 'convert //media/smb/Uploads/1995/April_TIFF/G-95-02-07.tif G-95-02-07-%03d.tif'
x = subprocess.run( [bashCmd + ';' + 'zip tmp.zip *.tif'],
                     cwd='/home/jghafa/archive/tmp/',
                     stdout=subprocess.PIPE,
                     shell=True)
print ('return ',x)    

