#!/usr/bin/python3

from openpyxl import load_workbook
from internetarchive import *
import pickle
import glob

# Key to the Council Proceedings Index spreadsheet
# Col B, row[1],  Bills[file_name][0], Meeting Type
# Col C, row[2],  Bills[file_name][1], Date
# Col D, row[3],  Bills[file_name][2], Notes


# Key to the Scanned Ordinance Index spreadsheet
# Col B, row[1],  Bills[file_name][0], Bill
# Col C, row[2],  Bills[file_name][1], Ord
# Col D, row[3],  Bills[file_name][2], Status
# Col G, row[6],  Bills[file_name][3], Desc
# Col N, row[13], Bills[file_name][4], Intro
# Col O, row[14], Bills[file_name][5], Final
# Col P, row[15], Bills[file_name][6], Notes

def build_Bills_dict (Bills, sheet):
    """ Read Excel Ordinance data sheet and append it to a dictionary"""
    ws = wb[sheet]
    for row in ws.rows:
        # ignore rows where column B does not look like G-70-01
        if  row[1].value is not None:
            if row[1].value[1] == '-' and row[1].value[4] == '-' :
                bill_data = (row[1].value,row[2].value,row[3].value,row[6].value,row[13].value,row[14].value,row[15].value)
                key = row[1].value.strip()
                try:
                    print (Bills[key][0],'duplicate key')
                except KeyError:
                    Bills[key] = bill_data
    return Bills

def build_Proceedings_dict (Proceedings, sheet):
    """ Read Excel Ordinance data sheet and append it to a dictionary"""
    Valid_Types = ['Council Proceeding','Other','Special']
    ws = wb[sheet]
    for row in ws.rows:
        # ignore rows where column B is not a valid meeting type
        if  row[1].value in Valid_Types:
            #date = row[2].value[6:9] + '-' + row[2].value[0:1] + '-' + row[2].value[3:4]
            # Regular Meeting
            if row[1].value == 'Council Proceeding':
                key =('CR-' + str(row[2].value.day).zfill(2)+ '-'
                            + str(row[2].value.month).zfill(2) + '-'
                            + str(row[2].value.year))
            # Organzational Meeting    
            elif row[1].value == 'Other':
                key =('CO-' + str(row[2].value.day).zfill(2)+ '-'
                            + str(row[2].value.month).zfill(2) + '-'
                            + str(row[2].value.year))
            # Special Meeting
            elif row[1].value == 'Special':
                key =('CS-' + str(row[2].value.day).zfill(2)+ '-'
                            + str(row[2].value.month).zfill(2) + '-'
                            + str(row[2].value.year))
            Proceedings[key] = (row[3].value)
    return Proceedings

def Link(Title,URL,Display):
    """ return a <a> link """
    link='<a title="'+Title+'" target="_blank" href="'+URL+'">'+Display+'</a>'
    return link

def hyperlink(url,friendly):
    '''  create a hyperlink for a CSV that Excel will read'''
    h1 = '=hyperlink("'
    h2 = '","'
    h3 = '")'
    hyper = h1 + url + h2 + friendly + h3
    # remove the " so Excel import it
    # the Excel user will have to replace them back
    #wrap the link in quotes
    return '"'+hyper.replace('"','~')+'"'

BillType = {'A':'Appropriation','G':'General','R':'Resolution',
           'S':'Special','X':'Annexation','Z':'Zoning'}
brk = '<br>'

Bills = {}

picklefile = 'CouncilVideo.pickle'

try:
    CouncilVideo = pickle.load(open(picklefile, "rb"))
except (OSError, IOError) as e:
    print ('dumping with pickle')
    CouncilVideo = [item.metadata['identifier'] for item in search_items('collection:(councilmeetings)').iter_as_items()]
    pickle.dump(CouncilVideo, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

# open log file
log = open('../Documents/Crosslink.txt', 'a')
log.write('Error,Bill,Intro,Intro Day,Final,Final Day,Notes' '\n')


#wb = load_workbook(filename =
#    '//vs-videostorage/City Council Ordinances/Council Proceedings Index.xlsx')
wb = load_workbook(filename = '/media/smb/Council Proceedings Index.xlsx')
#Proceedings = {}
#Proceedings = build_Proceedings_dict (Proceedings, 'Sheet1')
Bills = build_Proceedings_dict (Bills, 'Council Proceedings')
#print ('Bills=',Bills)

#wb = load_workbook(filename =
#    '//vs-videostorage/City Council Ordinances/Scanned Ordinance Index.xlsx')
wb = load_workbook(filename = '/media/smb/Scanned Ordinance Index.xlsx')

Bills = build_Bills_dict (Bills, '1970')
Bills = build_Bills_dict (Bills, '1971')
Bills = build_Bills_dict (Bills, '1995')

# Read the file names
PATH = '/media/smb/Uploads'

# get all the files in and under PATH
files = [file for file in glob.glob(PATH + '/**/*.*', recursive=True)]

dirlist = []
fn_list = []
for fn in files:
    fn_list.append(fn.split('/')[-1])
    dirlist.append(fn.rstrip(fn.split('/')[-1]))
    
print ()
# loop thru file names
for f in range(len(fn_list)):
    file_name, file_ext = fn_list[f].split('.')
    if file_name == 'Thumbs': continue  # this a windows junk file
    if not file_ext.upper() == 'TIF': continue # not a bill
    prefix = file_name.split('-')[0]
    if prefix in ['CR','CS','CO']: continue # this is a council proceeding

    bill = file_name.split(' ')[0]
    identifier = 'FWCityCouncil-Ordinance-'+bill
    title = 'Fort Wayne Ordinance '+bill
    mediatype = 'texts'
    collection = 'citycouncilordinances'

    print('identifier',identifier)
    try:
        if Bills[bill][6] is None:
            notes = ''
        else:
            notes = Bills[bill][6]
        print (bill,Bills[bill][4],Bills[bill][5])
        final = Bills[bill][5].strftime("%Y-%m-%d")

        #date = final

        if Bills[bill][4] is None:
            intro = 'The Intro date not available'
        else:
            intro = Bills[bill][4].strftime("%Y-%m-%d")

        desc = ('Bill: ' + bill + brk +
                'Type: ' + BillType[bill[0]] + brk +
                'Status: ' + Bills[bill][2] + brk +
                'Ordinance: ' + Bills[bill][1] + brk +
                Bills[bill][3] + brk +
                'Introduced: ' + intro + brk +
                'Final Disposition: ' + final)
        
        IntroID = 'FWCityCouncil-'+intro
        IntroLink =(Link(intro + ' Council Video',
            'https://archive.org/details/FWCityCouncil-'+intro,
            'Video of Council Introduction '+intro))
        
        if IntroID in CouncilVideo:
            IntroLink += brk
        else:
            if Bills[bill][4].year in range(1981,2007):
                log.write('Missing Intro Video,'+
                  hyperlink(dirlist[f].replace('/media/smb/','\\\\vs-videostorage\\City Council Ordinances\\').replace('/','\\') + fn_list[f],bill)+ ',' +
                  hyperlink('https://archive.org/details/FWCityCouncil-'+intro, intro) + ',' +
                  '"=datevalue(indirect(address(row(),column()-1,4)))"' + ',' +                
                  hyperlink('https://archive.org/details/FWCityCouncil-'+final, final) + ',' +
                  '"=datevalue(indirect(address(row(),column()-1,4)))"' + ',' +                
                  '\n')
            IntroLink = ''
                        
        FinalID = 'FWCityCouncil-'+final
        FinalLink =(Link(final + ' Council Video',
                'https://archive.org/details/FWCityCouncil-'+final,
                'Video of Council Introduction '+final) + brk)

        if FinalID in CouncilVideo:
            FinalLink += brk
        else:
            if Bills[bill][5].year in range(1981,2007):
                log.write('Missing Final Video,'+
                  hyperlink(dirlist[f].replace('/media/smb/','\\\\vs-videostorage\\City Council Ordinances\\').replace('/','\\') + fn_list[f],bill)+ ',' +
                  hyperlink('https://archive.org/details/FWCityCouncil-'+intro, intro) + ',' +
                  '"=datevalue(indirect(address(row(),column()-1,4)))"' + ',' +                
                  hyperlink('https://archive.org/details/FWCityCouncil-'+final, final) + ',' +
                  '"=datevalue(indirect(address(row(),column()-1,4)))"' + ',' +                
                  '\n')
            FinalLink = ''

        note = (IntroLink + FinalLink +
                'Document Notes:' + notes)

        subject='Fort Wayne;'+bill+';'+Bills[bill][1]


        print('File Path',dirlist[f]+fn_list[f])
        print(brk)
        print('title',title)
        print(brk)
        print(mediatype,collection,final,intro)
        print(brk)
        print(desc)
        print(brk)
        print(note)
        print(brk)
        print(subject)
                        
        #print(bill,Bills[bill][1],Bills[bill][2],Bills[bill][4],Bills[bill][5])
        print()
        print(brk)
        print(brk)
        
    except KeyError:
        print(dirlist[f], fn_list[f],'<<<<========== Not Found in spreadsheet')
    #z=input('file names')
log.close()
