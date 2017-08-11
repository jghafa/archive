''' check for tuesday'''
import datetime
from internetarchive import *
#import pickle


#picklefile = 'CouncilVideo.pickle'

#try:
#    CouncilVideo = pickle.load(open(picklefile, "rb"))
#except (OSError, IOError) as e:
#    print ('dumping with pickle')
#    CouncilVideo = [item.metadata['identifier'] for item in search_items('collection:(councilmeetings)').iter_as_items()]
#    pickle.dump(CouncilVideo, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)


for item in search_items('collection:(councilmeetings)').iter_as_items():
    #print(item.metadata['identifier'], item.metadata['date'])
    #print(item.metadata['identifier'].split('-'))
    id_year = item.metadata['identifier'].split('-')[1]
    for f in get_files(item.metadata['identifier'], glob_pattern='*.*4'):
        #print (f.name,f.name.split('-'))
        file_year = f.name.split('-')[0]
        if id_year[2:] == file_year:
            pass
            #print ('Years match')
        else:
            print ('Mismatch',f.name,item.metadata['identifier'])
    #z =input('pause')
