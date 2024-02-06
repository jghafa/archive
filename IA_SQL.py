#!/usr/bin/python3

import sqlite3

sql_file='/home/jghafa/archive/Council.sqlite'
SQLconn = sqlite3.connect(sql_file,timeout=30)
SQL = SQLconn.cursor()

def DropAddOrd():
    SQL.execute("""drop table if exists Ordinance;""")
    SQL.execute("""create table Ordinance (item text PRIMARY KEY, locked BOOL );""")

def DropAddProc():
    SQL.execute("""drop table if exists Proceeding;""")
    SQL.execute("""create table Proceeding (item text PRIMARY KEY, locked BOOL );""")

def DropAddVid():
    SQL.execute("""drop table if exists Video;""")
    SQL.execute("""create table Video (item text PRIMARY KEY, locked BOOL );""")

def CommitSQL():
    SQLconn.commit()

def CloseSQL():
    SQLconn.commit()
    SQLconn.close()
    
Lock=True
Unlock=False

def LockItem(itemtype, item, locked):
    ''' update the locked status of the item'''
    insstring = 'INSERT OR REPLACE into Ordinance values (?,?)'
    if itemtype[0].upper() == 'P':
        insstring = 'INSERT OR REPLACE into Proceeding values (?,?)'
    if itemtype[0].upper() == 'V':
        insstring = 'INSERT OR REPLACE into Video values (?,?)'
    SQL.execute(insstring,(item,locked) )
    SQLconn.commit()

def RemoveItem(itemtype, item):
    ''' Remove from SQL if upload failed '''
    selstring = 'DELETE FROM Ordinance WHERE item = (?);'
    if itemtype[0].upper() == 'P':
        selstring = 'DELETE FROM Proceeding WHERE item = (?);'
    if itemtype[0].upper() == 'V':
        selstring = 'DELETE FROM Video WHERE item = (?);'
    SQL.execute(selstring,(item,) )
    SQLconn.commit()

def ItemExist(itemtype, item):
    ''' Return True if the item exists, False if not '''
    selstring = 'SELECT * FROM Ordinance WHERE item = (?);'
    if itemtype[0].upper() == 'P':
        selstring = 'SELECT * FROM Proceeding WHERE item = (?);'
    if itemtype[0].upper() == 'V':
        selstring = 'SELECT * FROM Video WHERE item = (?);'
    for row in SQL.execute(selstring, (item,) ):
        return True
    return False

def Locked(itemtype, item):
    ''' Return True if the item exists, False if not '''
    selstring = 'SELECT locked FROM Ordinance WHERE item = (?);'
    if itemtype[0].upper() == 'P':
        selstring = 'SELECT locked FROM Proceeding WHERE item = (?);'
    if itemtype[0].upper() == 'V':
        selstring = 'SELECT locked FROM Video WHERE item = (?);'
    for row in SQL.execute(selstring, (item,) ):
	    return row[0]

def CountItem(itemtype, item='%'):
    ''' Return True if the item exists, False if not '''
    selstring = 'SELECT COUNT() FROM Ordinance WHERE item like (?);'
    if itemtype[0].upper() == 'P':
        selstring = 'SELECT COUNT() FROM Proceeding WHERE item like (?);'
    if itemtype[0].upper() == 'V':
        selstring = 'SELECT COUNT() FROM Video WHERE item like (?);'
    for row in SQL.execute(selstring, (item,) ):
	    return row[0]

def SearchItem(itemtype, item):
    ''' Return True if the item exists, False if not '''
    selstring = 'SELECT * FROM Ordinance WHERE item like (?);'
    if itemtype[0].upper() == 'P':
        selstring = 'SELECT * FROM Proceeding WHERE item like (?);'
    if itemtype[0].upper() == 'V':
        selstring = 'SELECT * FROM Video WHERE item like (?);'
    return SQL.execute(selstring, (item,) ).fetchall()

def SearchLock(itemtype, lock=True):
    ''' Return True if the item exists, False if not '''
    selstring = 'SELECT * FROM Ordinance WHERE locked = (?);'
    if itemtype[0].upper() == 'P':
        selstring = 'SELECT * FROM Proceeding WHERE locked = (?);'
    if itemtype[0].upper() == 'V':
        selstring = 'SELECT * FROM Video WHERE locked = (?);'
    return SQL.execute(selstring, (lock,) ).fetchall()

def UnlockAll(itemtype):
    for l in SearchLock(itemtype):
        LockItem(itemtype, l[0], Unlock)

def DeleteLockedAll(itemtype):
    for l in SearchLock(itemtype):
        RemoveItem(itemtype, l[0])

def StatusReport():
    # Item count
    print('Ord =',CountItem('Ord'))
    print('Locked Ord',len(SearchLock('Ord')))
    # Locked Ordinances
    for l in SearchLock('Ord'):
        print(l[0],'Locked')
        print(f"IA_SQL.LockItem('Ord', '{l[0]}', IA_SQL.Unlock)")
    if SearchItem('Ord','FWCityCouncil-Ordinance-A-69-11-19'):
        print('Successfull Ordinance Search')
    else:
        print('Ord Search Failed')
    print()
    # Proceeding Count
    print('Pro =',CountItem('Proc'))
    print('Locked Pro',len(SearchLock('Proc')))
    for l in SearchLock('Pro'):
        print(l[0],'Locked')
        print(f"IA_SQL.LockItem('Pro', '{l[0]}', IA_SQL.Unlock)")
    if SearchItem('Proc','FWCityCouncil-Proceedings-CS-1976-01-01'):
        print('Successfull Proceeding Search')
    else:
        print('Failed Proceeding Search')
    print()
    #Video Count
    print('Vid =',CountItem('Video'))
    print('Locked Vid',len(SearchLock('Vid')))
    for l in SearchLock('Vid'):
        print(l[0],'Locked')
        print(f"IA_SQL.LockItem('Vid', '{l[0]}', IA_SQL.Unlock)")
    print()
    # Print common commands
    print(f"import {__file__.split('/')[-1].split('.')[0]}")
    print(f"StatusReport()")

if __name__ == '__main__':
    StatusReport()
