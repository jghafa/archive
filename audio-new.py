#!/usr/bin/python
'''
upload audio files
'''

from __future__ import print_function
from internetarchive import *
from datetime import datetime
from time import strftime

# open log file
log = open('log'+datetime.now().strftime('%Y-%m-%d')+'.txt', 'a')
log.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S, ') + 
          ' Start' + '\n')


# Theses are the Fort Wayne collection names
#CollectionName = 'test_collection'
CollectionName = 'mayoraudiofiles'

# This metadata media type
vidmediatype = 'audio'

# Title of the item in the collection.  This is the one people see.
Title = ''

#Unique indentifer for the upload, becomes the IA directory name
Identifier = ''

#Vidio date, used for the metadata, formated ISO 8601
# yyyy-mm-dd
vidDate = ''

#video description, used for metadata, from spreadsheet via text file
vidDesc = "Mayor's Weekly Radio Spots"

#metadata for the producer
vidCreator = 'City of Fort Wayne, Indiana'

#metadata for the Creative Commons license
vidLicense = 'http://creativecommons.org/licenses/by-nc-sa/4.0/'

#metadata for search fields
vidSubject = ['Fort Wayne','Local Government','Mayor']

f = open('list1.csv', mode='r')

for line in f:
    filename = line.split(',')[0]
    date = line.split(',')[1].strip()
    if date == '':
        continue

    year = date.split('/')[2]
    month = date.split('/')[0]
    day = date.split('/')[1]
    #print (year,month.zfill(2),day.zfill(2))
    vidDate = year+ '-' +month.zfill(2)+ '-' +day.zfill(2)
    Title = filename.split('.')[0].strip()
    Identifier = Title.replace(" ", "-")
    md = dict(collection = CollectionName, 
              title      = Title,
              mediatype  = vidmediatype, 
              description= vidDesc,
              creator    = vidCreator,
              subject    = vidSubject,
              licenseurl = vidLicense, 
              date       = vidDate)

    #print (filename,  Title, Identifier, vidDate)
    #print (md)
    #continue
    #x = raw_input('paused')
    try:
        r = upload(Identifier, files=filename, metadata=md, 
                   retries=30, checksum=True) #retries_sleep=20,
        print ('Status code', r[0].status_code, filename)
        log.write (datetime.now().strftime('%Y-%m-%d %H:%M:%S, ') + 
                  filename +' uploaded' + '\n')
    except Exception as e:
        print ('Failed on ', filename, e.message, e.args)
        log.write (datetime.now().strftime('%Y-%m-%d %H:%M:%S, ') + 
                  filename +' failed' +  e.message + '\n\n')
        continue

    #x = raw_input('paused')

