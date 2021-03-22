#!/usr/bin/python3
"""
Clear the item lock in SQL
"""
import sqlite3
import argparse

def RemoveItem(itemtype, bill):
    ''' Remove from SQL if upload failed '''
    conn = sqlite3.connect('Council.sqlite')
    r = conn.cursor()
    selstring = 'DELETE FROM Ordinance WHERE item = (?);'
    if itemtype[0] == 'P':
        selstring = 'DELETE FROM FROM Proceeding WHERE item = (?);'
    if itemtype[0] == 'V':
        selstring = 'DELETE FROM FROM Video WHERE item = (?);'
    r.execute(selstring,(bill,) )
    conn.commit()
    conn.close()

parser = argparse.ArgumentParser()
parser.add_argument("coll_name", nargs='*', default=['Org'])
args = parser.parse_args()
# input_name is list of strings
input_arg = args.coll_name

SQLconn = sqlite3.connect('Council.sqlite')
SQL = SQLconn.cursor()

SQLstring = 'SELECT * FROM Ordinance WHERE locked <> 0;'
if input_arg[0] == 'P':
    SQLstring = 'SELECT * FROM Proceeding WHERE locked <> 0;'
if input_arg[0] == 'V':
    SQLstring = 'SELECT * FROM Video WHERE locked <> 0;'

for row in SQL.execute(SQLstring):
    print('Removing ', row[0])
    RemoveItem(input_arg, row[0] )

'''
SQL.execute("""drop table if exists Video;""")
SQL.execute("""create table Video (item text PRIMARY KEY, locked BOOL );""")
SQL.execute("""drop table if exists Ordinance;""")
SQL.execute("""create table Ordinance (item text PRIMARY KEY, locked BOOL );""")
SQL.execute("""drop table if exists Proceeding;""")
SQL.execute("""create table Proceeding (item text PRIMARY KEY, locked BOOL );""")
'''

"""
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
"""
