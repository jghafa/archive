#!/usr/bin/python3
"""
Check that AX has all the documents
"""

import glob
import IA_SQL

# Read the file names
PATH = '/media/smb/PDFs/'

# just the filename, no path, no .PDF
docs = [f.split('/')[-1].split('.')[0] for f in glob.glob(PATH + '**/*.[pP][dD][fF]')]

# Read the metadata from IA
print('These are the Internet Archive ordinances not in AX.')
#for c in CouncilOrdinance:
for row in IA_SQL.SearchItem('Ord','%'):
    c = row[0]
    if c in docs:
        continue
    print(c)

# Read the metadata from IA
print()
print('These are the Internet Archive proceedings not in AX.')
#for c in CouncilProceedings:
for row in IA_SQL.SearchItem('Pro','%'):
    c = row[0]
    if c in docs:
        continue
    print(c)
