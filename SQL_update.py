#!/usr/bin/python3
"""
Rebuild the SQL tables
"""

from internetarchive import *
import sqlite3

SQLconn = sqlite3.connect('new.Council.sqlite')
SQL = SQLconn.cursor()

SQL.execute("""drop table if exists Video;""")
SQL.execute("""create table Video (item text PRIMARY KEY, locked BOOL );""")
SQL.execute("""drop table if exists Ordinance;""")
SQL.execute("""create table Ordinance (item text PRIMARY KEY, locked BOOL );""")
SQL.execute("""drop table if exists Proceeding;""")
SQL.execute("""create table Proceeding (item text PRIMARY KEY, locked BOOL );""")
Lock=True
Unlock=False

def LockItem(itemtype, bill, locked):
    ''' update the locked status of the item'''
    insstring = 'INSERT OR REPLACE into Ordinance values (?,?)'
    if itemtype[0] == 'P':
        insstring = 'INSERT OR REPLACE into Proceeding values (?,?)'
    if itemtype[0] == 'V':
        insstring = 'INSERT OR REPLACE into Video values (?,?)'
    SQL.execute(insstring,(bill,locked) )
    SQLconn.commit()

def AddItem(itemtype, bill):
    ''' LockItem will create a record if does not exist'''
    LockItem(itemtype, bill, False)

def RemoveItem(itemtype, bill):
    ''' Remove from SQL if upload failed '''
    selstring = 'DELETE FROM Ordinance WHERE item = (?);'
    if itemtype[0] == 'P':
        selstring = 'DELETE FROM FROM Proceeding WHERE item = (?);'
    if itemtype[0] == 'V':
        selstring = 'DELETE FROM FROM Video WHERE item = (?);'
    SQL.execute(selstring,(bill,) )
    SQLconn.commit()

def ItemExist(itemtype, bill):
    ''' Return True if the item exists, False if not '''
    selstring = 'SELECT * FROM Ordinance WHERE item = (?);'
    if itemtype[0] == 'P':
        selstring = 'SELECT * FROM Proceeding WHERE item = (?);'
    if itemtype[0] == 'V':
        selstring = 'SELECT * FROM Video WHERE item = (?);'
    for row in SQL.execute(selstring, (bill,) ):
        return True
    return False

print ('Reading citycouncilordinance collection')
for item in search_items('collection:(citycouncilordinances)').iter_as_items():
	Id = item.metadata['identifier']
	print (Id)
	AddItem('O',Id)

print ('Reading citycouncilproceeding collection')
for item in search_items('collection:(citycouncilproceedings)').iter_as_items():
	Id = item.metadata['identifier']
	print (Id)
	AddItem('P',Id)

print ('Reading councilmeeting collection')
for item in search_items('collection:(councilmeetings)').iter_as_items():
	Id = item.metadata['identifier']
	print (Id)
	AddItem('V',Id)
