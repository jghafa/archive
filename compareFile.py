#!/usr/bin/python3
""" compare IA, spreadsheet, and SMB to check for mismatches
"""

from openpyxl import load_workbook
from internetarchive import *
# import pickle
import IA_SQL
import glob

def build_Bills_dict (Bills):
    """ Read Excel Ordinance data sheet and append it to a dictionary"""
    for ws in wb.worksheets:
        for row in ws.rows:
            # ignore rows where column B does not look like G-70-01
            if  row[1].value is not None and not row[1].data_type in 'b':
                if row[1].value[1] == '-' and row[1].value[4] == '-' :
                    bill_data = (row[1].value,row[2].value,row[3].value,row[6].value,row[13].value,row[14].value,row[15].value,ws)
                    key = row[1].value.strip()
                    try:
                        print (Bills[key][0],',Duplicate Meta Entries')
                    except KeyError:
                        Bills[key] = bill_data
                    if Bills[key][1] is None:
                        print (Bills[key][0],',Missing Ord Number')
                    if Bills[key][2] is None:
                        print (Bills[key][0],',Missing Bill Status')
                    if Bills[key][3] is None:
                        print (Bills[key][0],',Missing Bill Desc')
                    if Bills[key][4] is None:
                        print (Bills[key][0],',Missing Intro date')
                    if Bills[key][5] is None:
                        print (Bills[key][0],',Missing Final date')
    return Bills

print('Ordinance,Status,Desc')
Bills = {}
wb = load_workbook(filename = '/media/smb/Scanned Ordinance Index.xlsx')
Bills = build_Bills_dict (Bills)
XLSlist = list(Bills.keys())

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
    if len(filename.split('.')) > 2:
        print (filename, ',Period in filename')
    prefix = filename.split('-')[0]
    if prefix in ['CR','CS','CO']:
        continue # this is a council proceeding
    if ' .TIF' in filename.upper():
        print ('space before .TIF',fn)
    if len(filename) > 10:
        if not filename[10:11] in [' ','.']:
            print (filename, ',Missing space after ord name')

    fn_list.append(fn.split('/')[-1])
    dirlist.append(fn.rstrip(fn.split('/')[-1]))
    SMBlist.append(fn.split('/')[-1].split('.')[0])

#IAlist = []
#selstring = 'SELECT * FROM Ordinance;'
#for row in SQL.execute(selstring):
#	IAlist.append(row[0].lstrip('FWCityCouncil-Ordinance-'))

IAlist=[x.lstrip('FWCityCouncil-Ordinance-') for x,y in IA_SQL.SearchItem('Ord','%')]

SMBlist.sort()
IAlist.sort()
XLSlist.sort()

SMBindex = IAindex = XLSindex = 0
SMBlen = len(SMBlist)
IAlen = len(IAlist)
XLSlen = len(XLSlist)

while SMBindex < SMBlen and IAindex < IAlen and XLSindex < XLSlen:
    if (SMBlist[SMBindex] == IAlist[IAindex]
        and SMBlist[SMBindex] == XLSlist[XLSindex]):
        #all match
        print(SMBlist[SMBindex],',All entries exist,',Bills[SMBlist[SMBindex]][-1])
        SMBindex += 1
        XLSindex += 1
        IAindex += 1
        continue

    if (SMBlist[SMBindex] == IAlist[IAindex]):
        #SMB and IA match
        if XLSlist[XLSindex] < SMBlist[SMBindex]:
            #XLS low
            print(XLSlist[XLSindex],',XLS missing SMB & IA,Metadata Only',Bills[XLSlist[XLSindex]][-1])
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
            print(IAlist[IAindex],',IA missing SMB & XLS, IA Only')
            IAindex += 1
        else:
            print(SMBlist[SMBindex],',SMB & XLS missing IA,Missing IA',Bills[XLSlist[XLSindex]][-1])
            SMBindex += 1
            XLSindex += 1
        continue
            
    if (IAlist[IAindex] == XLSlist[XLSindex]):
        #IA and XLS match
        if  SMBlist[SMBindex] < IAlist[IAindex]:
            #SMB low
            print(SMBlist[SMBindex],',SMB missing IA & XLS, Local Only')
            SMBindex += 1
        else:
            print(IAlist[IAindex],',IA & XLS missing SMB,',Bills[XLSlist[XLSindex]][-1])
            IAindex += 1
            XLSindex += 1
        continue

    #no match, find the low ordinance
    lowOrd = min(SMBlist[SMBindex],XLSlist[XLSindex],IAlist[IAindex])
    if lowOrd == SMBlist[SMBindex]:
        print(SMBlist[SMBindex],',SMB missing IA & XLS, Local Only')
        SMBindex += 1

    if lowOrd == XLSlist[XLSindex]:
        print(XLSlist[XLSindex],',XLS missing SMB & IA,Metadata Only',Bills[XLSlist[XLSindex]][-1])
        XLSindex += 1

    if lowOrd == IAlist[IAindex]:
        print(IAlist[IAindex],',IA missing SMB & XLS, IA Only')
        IAindex += 1

print('SMB',SMBindex,SMBlen)
print('IA',IAindex,IAlen)
print('XLS',XLSindex,XLSlen)

if (IAindex == IAlen):
    while SMBindex < SMBlen and XLSindex < XLSlen:
        if XLSlist[XLSindex] == SMBlist[SMBindex]:
            print(SMBlist[SMBindex],',SMB & XLS but not IA,',Bills[XLSlist[XLSindex]][-1])
            SMBindex += 1
            XLSindex += 1
            continue
            
        if XLSlist[XLSindex] < SMBlist[SMBindex]:
            #XLS low
            print(XLSlist[XLSindex],',XLS but not SMB & IA,',Bills[XLSlist[XLSindex]][-1])
            XLSindex += 1
        else:
            print(SMBlist[SMBindex],',SMB but not IA & XLS, No Metadata')
            SMBindex += 1

print('SMB',SMBindex,SMBlen)
print('IA',IAindex,IAlen)
print('XLS',XLSindex,XLSlen)

while SMBindex < SMBlen :
    print(SMBlist[SMBindex],',SMB & XLS but not IA,',Bills[SMBlist[SMBindex]][-1])
    SMBindex += 1
            
while XLSindex < XLSlen:
    print(XLSlist[XLSindex],',XLS but not SMB & IA,',Bills[XLSlist[XLSindex]][-1])
    XLSindex += 1

