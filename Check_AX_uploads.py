#!/usr/bin/python3
"""
Check that AX has all the documents
"""

#from openpyxl import load_workbook
#from internetarchive import *
#import os
import glob
import pickle
#from datetime import datetime
#from time import strftime
#import subprocess
#import argparse

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


# Read the file names
PATH = '/media/smb/PDFs/'

# just the filename, no path, no .PDF
docs = [f.split('/')[-1].split('.')[0] for f in glob.glob(PATH + '**/*.[pP][dD][fF]')]


print('These are the Internet Archive ordinances not in AX.')


for c in CouncilOrdinance:
    if c in docs:
        continue
    print(c)

print()
print('These are the Internet Archive proceedings not in AX.')
for c in CouncilProceedings:
    if c in docs:
        continue
    print(c)
