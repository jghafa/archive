#!/usr/bin/python3
'''
Upload City Council video files to the Internet Archive.
Group by day of video, and include txt and PDF files.

Download document collections from the Internet Archive
Files will be placed in directory below the current directory,
with the same file name as the collection.

usage: Vid (YY)

YY is the two digit year.

If no year is supplied on the imput line, the program will stop.


How set up this program.
1   Find a linux machine, it will have python already.

2   Update linuxm, like so:
sudo apt-get update
sudo apt-get upgrade

3   Install pip, like so:
sudo apt-get install python-pip

4   Install Internet Archive code for Python with pip:
sudo pip install internetarchive

5   Copy the CAR files to a CAR directory under the program dir.

6   Mount the SAN video files.
    Add the following line to the end of /etc/fstab

//10.2.1.14/city\040council\040videos$  /media/vid  cifs  uid=jghafa,username=jghafa,domain=acfwad,iocharset=utf8,sec=ntlm  0  0

    sudo mount -a

    When the system boots, it will ask for the JGHAFA password to the SAN.
'''

from __future__ import print_function
from internetarchive import *
from datetime import datetime
from time import strftime
import os

def readtext (dirname, filename):
    '''
    Read the date and description from inside the car.txt file.
    '''
    desc = date = ''
    f = open(dirname + filename, mode='r')
    for line in f:
        if 'Desc      :' in line:
            desc = line.split(' : ')[1].strip()
        if 'Date      :' in line:
            olddate = line.split(' : ')[1].strip()
            month = olddate.split('/')[0]
            day   = olddate.split('/')[1]
            year  = olddate.split('/')[2]
            if year[0] == '0':
                year = '20' + year
            elif year[0] == '1':
                year = '20' + year
            else:
                year = '19' + year
            date = year + '-' + month +  '-' + day
    f.close()
    return (desc, date)


processyear = '34'

pdf = []
txt = []
vidcount = txtcount = pdfcount = 0
carRoot = 'CAR'
vidRoot = '/media/vid'
print ('Condition Assessment Report in ', carRoot)
print ('Video files in ', vidRoot)

for root, dirnames, filenames in os.walk(carRoot):
    for filename in filenames:
        if filename.endswith('.pdf'):
            pdf.append(filename)
        elif filename.endswith('.txt'):
            txt.append(filename)

print ('loading video names')
vid = {}
vidlist = []
for root, dirnames, filenames in os.walk(vidRoot):
    if '/Reports' in root:
        print('Reports')
        continue
    if '/DoNotUse' in root:
        continue
    vidlist.append(root)
    vidkey = ''
    for filename in filenames:
        try:
            vidkey = root.split('/')[4]
        except IndexError:
            print('IndexError', root)
            continue
        if filename.endswith(('_a.mp4','_a.md5')):
            vidlist.append(filename)
            vid[vidkey] = vidlist
    vidlist = []

vcount = 0
for v in vid:
	vcount += len(vid[v]) - 1
print(vcount, 'videos, ',len(pdf), 'PDFs, ',len(txt), 'texts, ')

#Name of the Internet Archive collection target for uploads
#CollectionName = 'test_collection'
CollectionName = 'councilmeetings'

# This metadata media type
vidmediatype = 'movies'

# Title of the item in the collection.  This is the one people see.
# Fort Wayne City Council yyyy-mm-dd
Title = ''

#Unique indentifer for the upload, becomes the IA directory name
# FWCityCouncil-yyyy-mm-dd
Identifier = ''

#Vidio date, used for the metadata, formated ISO 8601
# yyyy-mm-dd
vidDate = ''

#video description, used for metadata, from spreadsheet via text file
vidDesc = ''

#metadata for the producer
vidCreator = 'City of Fort Wayne, Indiana'

#metadata for the Creative Commons license
vidLicense = 'http://creativecommons.org/licenses/by-nc-sa/4.0/'

#metadata for search fields
vidSubject = ['Fort Wayne','Local Government','City Council']

# The list of file names to upload.
Files = []
processlist = []

# open log file
log = open('log'+processyear+'.txt', 'a')
log.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S, ') + 
          'log of ' + processyear + ' Start' + 
          datetime.now().strftime('%Y-%m-%d %H:%M:%S, ') +  
          CollectionName + ' collection' + '\n')

for v in sorted(vid):
    if processyear in v[0:2]:
        processlist.append(v)

for v in ['95-1']:
#for v in ['83-18', '83-41', '95-1','91-42','94-43','95-26','95-30','00-24']:
#for v in processlist :
    filelist = vid[v]
    vidDir = filelist[0]
    Title = 'Fort Wayne City Council'
    for f in filelist[1:]:
        Files.append(vidDir + '/'+ f)
        if f.split('_')[0] + '.txt' in txt:
            Files.append(carRoot + '/' + f.split('_')[0] + '.txt')
        else:
            print (f, 'Missing text')
        if f.split('_')[0] + '.pdf' in pdf:
            Files.append(carRoot + '/' + f.split('_')[0] + '.pdf')
        else:
            print (f, 'Missing PDF')
        vidDesc, vidDate = readtext (carRoot + '/', f.split('_')[0] + '.txt' )
	# change next line for test items
        Title = 'Fort Wayne City Council ' + vidDate  #+ 'test'
        Identifier = 'FWCityCouncil-' + vidDate       #+ 'test'
    print ('')
    print (strftime("%Y-%m-%d %H:%M:%S"), CollectionName, vidmediatype)
    print (Title, Identifier)
    print (vidDate, vidDesc)
    print (Files[0])
    md = dict(collection = CollectionName, 
              title      = Title,
              mediatype  = vidmediatype, 
              description= vidDesc,
              creator    = vidCreator,
              subject    = vidSubject,
              licenseurl = vidLicense, 
              date       = vidDate)

    for f in Files:

        try:
            r = upload(Identifier, files=f, metadata=md, 
                       retries=30, checksum=True) #retries_sleep=20,
            print ('Status code', r[0].status_code, f)
            log.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S, ') + 
                      f +' uploaded' + '\n')

        except Exception as e:
            print('Failed on ', f, e.message, e.args)
            log.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S, ') + 
                      f +' failed' +  e.message + '\n')
            continue

    print (strftime("%Y-%m-%d %H:%M:%S"))
    print ('')

    Files = []
    #raw_input(' ')

log.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S, ') + 
          'log '+processyear+' finish' + '\n')
log.close()
