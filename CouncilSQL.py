#!/usr/bin/python3
""" Create a SQLite database of  items uploaded to Internet Archive
This replaces a three pickle files and will add the abilty for update programs to run together
"""

print('Council SQL insertion')
import pickle
import sqlite3
from internetarchive import *

#Define the database. The database is completely rebuilt every program run.
SQLconn = sqlite3.connect('Council.sqlite')
SQL = SQLconn.cursor()

SQL.execute("""drop table if exists Video;""")
SQL.execute("""create table Video (item text PRIMARY KEY );""")
SQL.execute("""drop table if exists Ordinance;""")
SQL.execute("""create table Ordinance (item text PRIMARY KEY );""")
SQL.execute("""drop table if exists Proceeding;""")
SQL.execute("""create table Proceeding (item text PRIMARY KEY );""")

print('Reading Videos')
picklefile = 'CouncilVideo.pickle'
try:
    CouncilVideo = pickle.load(open(picklefile, "rb"))
except (OSError, IOError) as e:
    print ('Reading council video collection')
    CouncilVideo = [item.metadata['identifier'] for item in search_items('collection:(councilmeetings)').iter_as_items()]
    #pickle.dump(CouncilVideo, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

print('Reading Ordinances')
picklefile = 'CouncilOrdinance.pickle'
try:
    CouncilOrdinance = pickle.load(open(picklefile, "rb"))
except (OSError, IOError) as e:
    print ('Reading citycouncil ordinance collection')
    CouncilOrdinance = [item.metadata['identifier'] for item in search_items('collection:(citycouncilordinances)').iter_as_items()]
    #pickle.dump(CouncilOrdinance, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

print('Reading Proceedings')
picklefile = 'CouncilProceedings.pickle'
try:
    CouncilProceedings = pickle.load(open(picklefile, "rb"))
except (OSError, IOError) as e:
    print ('Reading citycouncil proceeding collection')
    CouncilProceedings = [item.metadata['identifier'] for item in search_items('collection:(citycouncilproceedings)').iter_as_items()]
    #pickle.dump(CouncilProceedings, open(picklefile, "wb"), protocol=pickle.HIGHEST_PROTOCOL)



#Insert the items in the database
print('Loading SQL')
tups = [(element,) for element in CouncilVideo]
SQL.executemany('INSERT OR IGNORE into Video values (?)', tups )
tups = [(element,) for element in CouncilOrdinance]
SQL.executemany('INSERT OR IGNORE into Ordinance values (?)', tups )
tups = [(element,) for element in CouncilProceedings]
SQL.executemany('INSERT OR IGNORE into Proceeding values (?)', tups )

#Save the database
SQLconn.commit()
print('Done')
