#!/usr/bin/python3
"""
Upload SoundCloud Wav files to IA

1) Get the files from \\san\gov\office of the mayor\office of the mayor\PIO\RadioSpots
2) Copy to a spot accessable fro here, like /media/smb/TestDVD/MayorAudio/
3) Make sure the file modification dates are correct for IA
4) Run mayorAudioFiles.py
"""

#import shutil
import glob
import os
import datetime
from internetarchive import *

PATH = '/media/smb/TestDVD/MayorAudio/'


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


for file_name in glob.glob(PATH + '*.[wW][aA][vV]'):
    try:
        mtime = os.path.getmtime(file_name)
    except OSError:
        print ('Not uploading ',file_name)
        continue
    last_modified_date = datetime.datetime.fromtimestamp(mtime)

    newname = 'RadioSpot '+file_name.split('/')[-1]
    Identifier = (newname.replace('.wav','').
                          replace(',','-').
                          replace(' - ','-').
                          replace('- ','-').
                          replace("&",'').
                          replace(';','-').
                          replace('.','-').
                          replace(' ','-').
                          replace('---','-').
                          replace('--','-').
                          replace('--','-').
                          replace("'",'')  )

    vidDate = datetime.datetime.strftime(last_modified_date,'%Y-%m-%d')
    Title = newname.replace('.wav','').strip()
    
    md = dict(collection = CollectionName, 
              title      = Title,
              mediatype  = vidmediatype, 
              description= vidDesc,
              creator    = vidCreator,
              subject    = vidSubject,
              licenseurl = vidLicense, 
              date       = vidDate)

    try:
        r = upload(Identifier, files=file_name, metadata=md, 
                   retries=30, checksum=True) #retries_sleep=20,
        print ('Status code', r[0].status_code, Identifier)
    except Exception as e:
        print ('Failed on ', Identifier, e.message, e.args)
