#!/usr/bin/python3
""" Proceedings: compare IA, spreadsheet, and SMB to check for mismatches
"""

from openpyxl import load_workbook
from internetarchive import *
import os
import glob
import IA_SQL
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("coll_name", nargs='*', default=['1969']) 
input_name = parser.parse_args().coll_name

ProcType = {'CR':'Regular','CO':'Organizational','CS':'Special'}

def build_Proceedings_dict (sheet):
    """ Read Excel Ordinance data sheet and append it to a dictionary"""
    Valid_Types = ['Council Proceeding','Other','Special']
    ws = wb[sheet]
    Proceedings = {}
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
            if row[3].value is None:
                Proceedings[key] = ('')
            else:
                Proceedings[key] = (row[3].value)
    return Proceedings

print('Loading Metadata',end='\r')
wb = load_workbook(filename = '/media/smb/Council Proceedings Index.xlsx')
Procs = build_Proceedings_dict ('Council Proceedings')

print('Loading file names',end='\r')
# open file
targetDir='/media/smb/PDFs/Proc'+ input_name[0] + '/'
os.makedirs(targetDir, exist_ok=True)

Moved = []

with open(targetDir+'AXUpload-Proc-'+input_name[0]+'.txt', 'w') as AXlink:
    # get all the files in and under PATH
    PATH = '/media/smb/Uploads'
    files = [file for file in glob.glob(PATH + '/**/*.*', recursive=True)]

    for fn in files:
        filename = (fn.split('/')[-1])
        if filename == 'Thumbs.db':
            continue  # this a windows junk file
        if not filename.split('.')[-1].upper() == 'TIF':
            continue # not a bill
        if 'INDEX' in filename.upper():
            continue
        if ' .TIF' in filename.upper():
            print (filename, ',space before .TIF')
        if len(filename.split('.')) > 2:
            print (filename, ',Period in filename')
            
        # CR-04-14-1970
        spd_name = fn.split('/')[-1].split('.')[0].split(' ')[0]
        # trailing is a list, in case there are extra - in spd_name
        p_type,p_mon,p_day,*trailing = spd_name.split('-')
        p_yr = trailing[0]
        p_name = p_type + '-' + p_yr + '-' + p_mon + '-' + p_day

        if p_type in ['CR','CS','CO']:
            if p_yr in input_name or p_name in input_name:
                Identifier = 'FWCityCouncil-Proceedings-'+p_name
                if Identifier in Moved:
                    continue  #There might be multiple copies in SMB
                # Get the PDF from IA
                print(Identifier, 'Downloading',end='\r')
                item = get_item(Identifier)
                item.download(glob_pattern='*.pdf',destdir=targetDir,no_directory=True,retries=10)

                meta =(       p_mon+'/'+p_day+'/'+p_yr
                        +'|' +ProcType[p_type]
                        +'|' +Procs[spd_name].replace('\n',' ')
                        +'|' 
                        +'\n')
                print(Identifier, 'Complete   ',end='\r')
                AXlink.write(meta)
                AXlink.write('@@'+targetDir+Identifier+'.PDF'+'\n')
                Moved.append(Identifier)
#######################################################
                
    for fn in files:
        filename = (fn.split('/')[-1])
        # Indexes only in this section
        if not 'INDEX' in filename.upper():
            continue
        
        if filename == 'Thumbs.db':
            continue  # this a windows junk file
        if not filename.split('.')[-1].upper() == 'TIF':
            continue # not a bill
            
        # Index-1968 Council Proceedings
        # Index-1969 Council Proceedings 1-100
        # Index-1969 Council Proceedings 101-145
        spd_name = fn.split('/')[-1].split('.')[0].split(' ')[0]
        # 
        indexname, indexyear = spd_name.split(' ')[0].split('-')
        if not indexname in "Index":
            # non standard format
            print('non standed index format')
            continue
        if not indexyear in input_name:
            # wrong year
            continue
        Identifier = 'FWCityCouncil-Proceedings-'+indexname+'-'+indexyear
        if Identifier in Moved:
            continue  #There might be multiple copies in SMB
        

        print(Identifier, 'Downloading',end='\r')
        item = get_item(Identifier)
        item.download(glob_pattern='*.pdf',destdir=targetDir,no_directory=True,retries=10)

        meta =('Council Proceedings for ' +
                indexyear +
                '\n')
        print(Identifier, 'Complete   ',end='\r')
        AXlink.write(meta)
        AXlink.write('@@'+targetDir+Identifier+'.PDF'+'\n')
        Moved.append(Identifier)


print()
