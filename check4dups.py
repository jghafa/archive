#import os
import glob
from collections import Counter

#os.chdir('//vs-videostorage/City Council Ordinances/Uploads')

FN_dict = {'A':'Appropriation','G':'General','R':'Resolution','S':'Special','X':'Annexation','Z':'Zoning'}

#PATH = '//vs-videostorage/City Council Ordinances/Uploads'
PATH = '/media/smb/Uploads'
# PATH/     the dir
# **/       every file and dir under PATH
# *.txt     every file that ends with '.txt'	

# get all the files under path
files = [file for file in glob.glob(PATH + '/**/*.*', recursive=True)]

# Count file names, i.e. the last split
duplist = Counter([fn.split('/')[-1] for fn in files ])

dirlist = []
fn_list = []
for fn in files:
    filename = fn.split('/')[-1]
    fn_list.append(filename)
    dirname = fn.rstrip(fn.split('/')[-1])
    dirlist.append(dirname)

pdf_count = tif_count = dup_count = fn_count = 0

for x in range(len(fn_list)):
    # don't worry about Thumbs
    if fn_list[x] == 'Thumbs.db': continue

    # don't worry about council proceedings
    key = fn_list[x].split('-')[0].upper()        
    if key in ['CR','CS','CO']: continue
    
#   check for a known ordinance type
    try:
        temp = FN_dict[key]
    except KeyError:
        print('unknown ordinance',dirlist[x],fn_list[x])


#   check for a PDF
    if fn_list[x].split('.')[-1].upper() == 'PDF':
        pdf_count += 1
        print('PDF',dirlist[x],fn_list[x])
        
    if fn_list[x].split('.')[-1].upper() == 'TIF':
        tif_count += 1
        # find PDF to match
        bill = fn_list[x].split('.')[0]
        blueprints = [b for b in fn_list if 'blueprint' in b and bill in b]
        if blueprints:
            [print (' bp=',f) for f in blueprints]
        
    fn_count += 1
    
    # found a duplicate file name
    if duplist [fn_list[x]] > 1:
        dup_count += 1
        print ('dup',fn_list[x], dirlist[x])

print('Searched',fn_count,'files for duplicate file names')
print('PDF', pdf_count)
print('Tif', tif_count)
print('Dups', dup_count)
