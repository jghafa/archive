#!/usr/bin/python3
'''
Modify the metadata for a council video item in our collection
'''
from internetarchive import *
from datetime import datetime

# retrieve the items in a collection
#for item in search_items('collection:(mayoraudiofiles)').iter_as_items():
for item in search_items('uploader:(jameshaley) AND title:(*test)').iter_as_items():
    print(item.metadata['identifier'], item.metadata['date'], item.metadata['notes'])
    newNotes = (datetime.now().strftime('%Y-%m-%d %H:%M:%S, ') +
                '<a title="1986-03-04 Council Video" target="_blank" href="https://archive.org/details/FWCityCouncil-1986-03-04">1986-03-04 Council Meeting</a>')
    r = item.modify_metadata(dict(notes=newNotes))
    print (r,' update status ')
