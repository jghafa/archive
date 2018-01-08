#!/usr/bin/python3
"""
Upload SoundCloud Wav files to IA
This version uses a spreadsheet to hold creations dates for the files
"""

import shutil
import glob
import os
from internetarchive import *

PATH = '/media/smb/TestDVD/MayorAudio/'
tmpDir = '/home/jghafa/archive/tmp/'

#Name of the Internet Archive collection target for uploads
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

f = open(PATH + 'list2.csv', mode='r')

for line in f:
    filename = line.split(',')[0]
    date = line.split(',')[1].strip()
    if date == '':
        continue
    newname = 'RadioSpot '+filename.replace(' ~by MayorFW [soundtake.net]','').replace(';','-')
    Identifier = newname.replace(' - ','-').replace('- ','-').replace(' ','-').replace('.wav','')
    shutil.copyfile(PATH+filename, tmpDir+newname)

    year = date.split('/')[2]
    month = date.split('/')[0]
    day = date.split('/')[1]

    vidDate = year+ '-' +month.zfill(2)+ '-' +day.zfill(2)
    Title = newname.split('.')[0].strip()

    md = dict(collection = CollectionName, 
              title      = Title,
              mediatype  = vidmediatype, 
              description= vidDesc,
              creator    = vidCreator,
              subject    = vidSubject,
              licenseurl = vidLicense, 
              date       = vidDate)

    #print (Identifier)
    #print (Title)
    #print (vidDate)
    #print (md)

    try:
        r = upload(Identifier, files=tmpDir+newname, metadata=md, 
                   retries=30, checksum=True) #retries_sleep=20,
        print ('Status code', r[0].status_code, newname)
    except Exception as e:
        print ('Failed on ', filename, e.message, e.args)



    for tmpfile in glob.glob(tmpDir + '*.[wW][aA][vV]'):
        os.remove(tmpfile)
