#!/usr/bin/python3
""" Proceedings: compare IA, spreadsheet, and SMB to check for mismatches
"""

from openpyxl import load_workbook
from internetarchive import *
import pickle
import glob

def build_Proceedings_dict (Proceedings, sheet):
    """ Read Excel Ordinance data sheet and append it to a dictionary"""
    Valid_Types = ['Council Proceeding','Other','Special']
    ws = wb[sheet]
    for row in ws.rows:
        # ignore rows where column B is not a valid meeting type
        if  row[1].value in Valid_Types:

            # Regular Meeting
            if row[1].value == 'Council Proceeding':
                key =('CR-' + str(row[2].value.month).zfill(2) + '-'
                            + str(row[2].value.day).zfill(2)+ '-'
                            + str(row[2].value.year))
            # Organzational Meeting    
            elif row[1].value == 'Other':
                key =('CO-' + str(row[2].value.month).zfill(2) + '-'
                            + str(row[2].value.day).zfill(2)+ '-'
                            + str(row[2].value.year))
            # Special Meeting
            elif row[1].value == 'Special':
                key =('CS-' + str(row[2].value.month).zfill(2) + '-'
                            + str(row[2].value.day).zfill(2)+ '-'
                            + str(row[2].value.year))
            Proceedings[key] = (row[3].value)
    return Proceedings

Procs = {}
wb = load_workbook(filename = '/media/smb/Council Proceedings Index.xlsx')
Procs = build_Proceedings_dict (Procs, 'Council Proceedings')
XLSlist = list(Procs.keys())

picklefile = 'CouncilProceedings.pickle'
try:
    CouncilProceedings = pickle.load(open(picklefile, "rb"))
except (OSError, IOError) as e:
    print ('Reading citycouncilordinance collection')
    CouncilProceedings = [item.metadata['identifier'] for item in search_items('collection:(citycouncilproceedings)').iter_as_items()]
    pickle.dump(CouncilProceedings, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

# Read the file names
PATH = '/media/smb/Uploads'

# get all the files in and under PATH
files = [file for file in glob.glob(PATH + '/**/*.*', recursive=True)]

dirlist = []
fn_list = []
SMBlist = []
for fn in files:
    filename = (fn.split('/')[-1])
    if filename == 'Thumbs.db':
        continue  # this a windows junk file
    if not filename.split('.')[-1].upper() == 'TIF':
        continue # not a bill
    if ' .TIF' in filename.upper():
        print (filename, ',space before .TIF')
    p_type = filename.split('-')[0]
    if not p_type in ['CR','CS','CO']:
        continue # this is a council proceeding
    p_mon  = filename.split('-')[1]
    p_day  = filename.split('-')[2]
    p_yr   = filename.split('-')[3]

    p_name = p_type + '-' + p_yr + '-' + p_mon + '-' + p_day

    fn_list.append(fn.split('/')[-1])
    dirlist.append(fn.rstrip(fn.split('/')[-1]))
    SMBlist.append(fn.split('/')[-1].split('.')[0])

IAlist=[x[26:29]+x[34:]+x[28:33] for x in CouncilProceedings]

SMBlist.sort()
IAlist.sort()
XLSlist.sort()

SMBindex = IAindex = XLSindex = 0
SMBlen = len(SMBlist)
IAlen = len(IAlist)
XLSlen = len(XLSlist)

#print('CouncilProceedings=', CouncilProceedings)
#print('IAlist=', IAlist)

print('Proceedings,Status,Desc')

while SMBindex < SMBlen and IAindex < IAlen and XLSindex < XLSlen:
    if (SMBlist[SMBindex] == IAlist[IAindex]
        and SMBlist[SMBindex] == XLSlist[XLSindex]):
        #all match
        print(SMBlist[SMBindex],',All entries exist,')
        SMBindex += 1
        XLSindex += 1
        IAindex += 1
        continue

    if (SMBlist[SMBindex] == IAlist[IAindex]):
        #SMB and IA match
        if XLSlist[XLSindex] < SMBlist[SMBindex]:
            #XLS low
            print(XLSlist[XLSindex],',XLS missing SMB & IA,Metadata Only')
            XLSindex += 1
        else:
            print(SMBlist[SMBindex],',SMB & IA missing XLS, No Metadata')
            SMBindex += 1
            IAindex += 1
        continue
            
    if (SMBlist[SMBindex] == XLSlist[XLSindex]):
        #SMB and IA match
        if IAlist[IAindex] < SMBlist[SMBindex]:
            #IA low
            print(IAlist[IAindex],',IA missing SMB & XLS,Local only')
            IAindex += 1
        else:
            print(SMBlist[SMBindex],',SMB & XLS missing IA,')
            SMBindex += 1
            XLSindex += 1
        continue
            
    if (IAlist[IAindex] == XLSlist[XLSindex]):
        #IA and XLS match
        if  SMBlist[SMBindex] < IAlist[IAindex]:
            #SMB low
            print(SMBlist[SMBindex],',SMB missing IA & XLS, No Metadata')
            SMBindex += 1
        else:
            print(IAlist[IAindex],',IA & XLS missing SMB,')
            IAindex += 1
            XLSindex += 1
        continue

    #no match, find the low ordinance
    lowOrd = min(SMBlist[SMBindex],XLSlist[XLSindex],IAlist[IAindex])
    if lowOrd == SMBlist[SMBindex]:
        print(SMBlist[SMBindex],',SMB but not IA & XLS,Local Only')
        SMBindex += 1

    if lowOrd == XLSlist[XLSindex]:
        print(XLSlist[XLSindex],',XLS missing SMB & IA,Metadata Only')
        XLSindex += 1

    if lowOrd == IAlist[IAindex]:
        print(IAlist[IAindex],',IA missing SMB & XLS,IA only')
        IAindex += 1

print('SMB',SMBindex,SMBlen)
print('IA',IAindex,IAlen)
print('XLS',XLSindex,XLSlen)

if (IAindex == IAlen):
    while SMBindex < SMBlen and XLSindex < XLSlen:
        if XLSlist[XLSindex] == SMBlist[SMBindex]:
            print(SMBlist[SMBindex],',SMB & XLS but not IA,Ready to upload')
            SMBindex += 1
            XLSindex += 1
            continue
            
        if XLSlist[XLSindex] < SMBlist[SMBindex]:
            #XLS low
            print(XLSlist[XLSindex],',XLS but not SMB & IA,Metadata Only')
            XLSindex += 1
        else:
            print(SMBlist[SMBindex],',SMB but not IA & XLS,Local Only')
            SMBindex += 1

print('SMB',SMBindex,SMBlen)
print('IA',IAindex,IAlen)
print('XLS',XLSindex,XLSlen)

while SMBindex < SMBlen :
    print(SMBlist[SMBindex],',SMB & XLS but not IA,Ready to upload')
    SMBindex += 1
            
while XLSindex < XLSlen:
    print(XLSlist[XLSindex],',XLS but not SMB & IA,Metadata Only')
    XLSindex += 1

