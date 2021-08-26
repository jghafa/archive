#!/usr/bin/python3
"""
Check that AX has all the documents
"""

#from openpyxl import load_workbook
#from internetarchive import *
#import os
import glob
#import pickle
import sqlite3
#from datetime import datetime
#from time import strftime
#import subprocess
#import argparse

"""
picklefile = 'CouncilProceedings.pickle'
try:
    CouncilProceedings = pickle.load(open(picklefile, "rb"))
except (OSError, IOError) as e:
    print ('Reading citycouncilproceeding collection')
    CouncilProceedings = [item.metadata['identifier'] for item in search_items('collection:(citycouncilproceedings)').iter_as_items()]
    pickle.dump(CouncilProceedings, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

picklefile = 'CouncilOrdinance.pickle'
try:
    CouncilOrdinance = pickle.load(open(picklefile, "rb"))
except (OSError, IOError) as e:
    print ('Reading citycouncilordinance collection')
    CouncilOrdinance = [item.metadata['identifier'] for item in search_items('collection:(citycouncilordinances)').iter_as_items()]
    pickle.dump(CouncilOrdinance, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)
"""

SQLconn = sqlite3.connect('Council.sqlite')
SQL = SQLconn.cursor()

# Read the file names
PATH = '/media/smb/PDFs/'

# just the filename, no path, no .PDF
docs = [f.split('/')[-1].split('.')[0] for f in glob.glob(PATH + '**/*.[pP][dD][fF]')]

# Read the metadata from IA
SQLstring = 'SELECT * FROM Ordinance WHERE locked = 0'

print('These are the Internet Archive ordinances not in AX.')
#for c in CouncilOrdinance:
for row in SQL.execute(SQLstring):
    c = row[0]
    if c in docs:
        continue
    print(c)

# Read the metadata from IA
SQLstring = 'SELECT * FROM Proceeding WHERE locked = 0'

print()
print('These are the Internet Archive proceedings not in AX.')
#for c in CouncilProceedings:
for row in SQL.execute(SQLstring):
    c = row[0]
    if c in docs:
        continue
    print(c)
