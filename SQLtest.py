#!/usr/bin/python3
""" Test Insert
Create a SQLite database of  items uploaded to Internet Archive
This replaces a three pickle files and will add the abilty for update programs to run together
"""

print('SQL insertion test')
import sqlite3
from internetarchive import *

#Define the database. The database is completely rebuilt every program run.
SQLconn = sqlite3.connect('Council.sqlite')
SQL = SQLconn.cursor()


#SQL.execute("""drop table if exists Proceeding""")
#SQL.execute("""
#        create table Proceeding (
#            item text PRIMARY KEY);
#          """)

while True:
	x = input('> ')
	if x == 'zzz':
		break
	SQL.execute('INSERT into Proceeding values (?)',(x,) )
	SQLconn.commit()
	SQL.execute('SELECT item FROM Proceeding ;')
	data = SQL.fetchall()
	for d in data:
		print(d)

while True:
	x = input('Search> ')
	if x == 'zzz':
		break
	SQL.execute('SELECT item FROM Proceeding WHERE item = (?);', (x,) )
	data = SQL.fetchone()
	if data is None:
		print('No data found')
	else:
		print(data)


#Save the database
SQLconn.commit()
print('Done')
