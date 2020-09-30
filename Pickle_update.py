#!/usr/bin/python3
"""
Update the pickle files
"""

from internetarchive import *
import pickle

picklefile = 'CouncilProceedings.pickle'
print ('Reading citycouncilproceeding collection')
CouncilProceedings = [item.metadata['identifier'] for item in search_items('collection:(citycouncilproceedings)').iter_as_items()]
print('Creating the pickle file')
pickle.dump(CouncilProceedings, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

picklefile = 'CouncilOrdinance.pickle'
print ('Reading citycouncilordinance collection')
CouncilOrdinance = [item.metadata['identifier'] for item in search_items('collection:(citycouncilordinances)').iter_as_items()]
print('Creating the pickle file')
pickle.dump(CouncilOrdinance, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

picklefile = 'CouncilVideo.pickle'
print ('Reading councilmeeting collection')
CouncilVideo = [item.metadata['identifier'] for item in search_items('collection:(councilmeetings)').iter_as_items()]
print('Creating the pickle file')
pickle.dump(CouncilVideo, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

'''
for item in search_items('collection:(citycouncilordinances)').iter_as_items():
	print (item)
	test = item.metadata['identifier']
	print (test)
	CouncilOrdinance.append(test)
'''
