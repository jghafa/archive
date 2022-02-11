#!/usr/bin/python3

from internetarchive import *
import sqlite3
import IA_SQL # my own module for tracking uploaded documents with sqlite3
import glob
import argparse
from datetime import datetime
from time import strftime

# True for uploading files, false for debugging
update_IA = True

parser = argparse.ArgumentParser()
parser.add_argument("coll_name", nargs='*', default=['2007-07-17'])
args = parser.parse_args()
# input_name is a list of strings
input_name = args.coll_name[0] # just the first string

#Name of the Internet Archive collection target for uploads
TestIdSuffix = ''   #Set to '' when testing is done
#CollectionName = 'test_collection'
CollectionName = 'councilmeetings'


# Title of the item in the collection.  This is the one people see.
Title = ''

#Unique indentifer for the upload, becomes the IA directory name
Identifier = ''

# Formatted ISO 8601, yyyy-mm-dd
Date = ''
Desc = ''
Notes= ''

# Fixed Internet Archive metadata fields
MediaType = 'movies'
Creator = 'City of Fort Wayne, Indiana'
License = 'http://creativecommons.org/licenses/by-nc-sa/4.0/'
Subject = ['Fort Wayne','Local Government','City Council']

def readNotes(filename):
    try:
        with open(filename, mode='r') as f:
            return f.read().replace('\n','<br />')
    except FileNotFoundError:
        return ''
    
def Link(Title,URL,Display):
    """ return a <a> link """
    link='<a title="'+Title+'" target="_blank" href="'+URL+'">'+Display+'</a>'
    return link

brk = '<br />'

# Read the file names
PATH = '/media/smb/DVD'

#tmpDir = tempfile.mkdtemp(dir='/home/jghafa/archive/tmp',prefix='Ord-U-')+'/'

# get all the files in
files = [file for file in glob.glob(PATH + '/*.[mP][pP][4]')]

fn_list = []
for fn in files:
    if len(fn.split('-')) == 5:
        vtype, vyear, vmon, vday, vext = fn.split('/')[-1].split('-')
        if (vtype+'-'+vyear+'-'+vmon+'-'+vday) not in fn_list:
            fn_list.append(vtype+'-'+vyear+'-'+vmon+'-'+vday)
vext=''

for fname in fn_list:
    if len(fname.split('-')) == 4:
        vtype, vyear, vmon, vday = fname.split('-')
        vidDate = vyear + '-' + vmon + '-' + vday
    else:
        print('bad file name',fname)
        continue  # file name not correct
    
    Title = 'Fort Wayne City Council ' + vidDate + TestIdSuffix
    Identifier = 'FWCityCouncil-'      + vidDate + TestIdSuffix
    Desc = 'Fort Wayne City Council Meeting on ' + vidDate
    Notes = readNotes(PATH+'/'+vtype+'-'+vidDate+'-Notes.txt')

    Upload_Doc = False
    if len(input_name) == 4:  # we want the whole year
        if input_name in vidDate: # the year matches
            if not IA_SQL.ItemExist('Vid', Identifier): # Not uploaded yet
                Upload_Doc = True
            else:
                if IA_SQL.Locked('Vid', Identifier): # Uploaded failed, so still locked
                    Upload_Doc = True
  	    
    if input_name == vidDate:  # we have one specific date to upload
        Upload_Doc = True    	    

    if not Upload_Doc:
        print('Skipping',Identifier,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        continue

    IA_SQL.LockItem('Vid', Identifier, IA_SQL.Lock)
    print('')
    print('Identifier',Identifier,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('File Path ',fname)

    md = dict(  collection = CollectionName, 
                title      = Title,
                mediatype  = MediaType, 
                description= Desc,
                creator    = Creator,
                subject    = Subject,
                licenseurl = License,
                notes      = Notes,
                date       = vidDate)

    for m in md:
        print(m.ljust(12), md[m])

    convertList  = glob.glob(PATH + '/*' + vidDate + '*.[mP][pP][4]' )
    convertList += glob.glob(PATH + '/*' + vidDate + '*.[tT][xX][tT]')
    for c in convertList:

        if update_IA:
            try:
                r = upload(Identifier, files=c, metadata=md, 
                           retries=30, checksum=True) #retries_sleep=20,
                print ('Status', r[0].status_code, c)
                IA_SQL.LockItem('Vid', Identifier, IA_SQL.Unlock)

            except Exception as e:
                print('Upload Failed on ', zipFile, e.message, e.args)
                IA_SQL.RemoveItem('Vid', Identifier)
                continue
        else:
            print('File ',c)
            z=input('update_IA is False')
