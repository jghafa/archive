#!/usr/bin/python3
import subprocess
import os

tmpDir = '/home/jghafa/archive/tmp/'
f = open('/media/smb/TestDVD/PDhtml.txt', 'r')

for line in f:
    if '<a href=' in line:
        link = line.split('"')[1]
        Cmd = 'wget '+link
        print(Cmd)
        x = subprocess.run([Cmd],
                     cwd=tmpDir,
                     stdout=subprocess.DEVNULL,
                     shell=True)

        filename = link.split('/')[-2]
        print(filename)
        name = line.split('>')[1].rstrip('</a')
        desc = line.split('>')[2].replace('/','-')
        print('"'+name+''+desc.rstrip()+'.html"')
        try:
            os.rename(tmpDir+'index.html',
                      tmpDir+name+''+desc.rstrip()+'.html')
        except FileNotFoundError:
            pass
        try:
            os.rename(tmpDir+filename,
                      tmpDir+name+''+desc.rstrip()+'.html')
        except FileNotFoundError:
            pass
        #x=input('pause')
