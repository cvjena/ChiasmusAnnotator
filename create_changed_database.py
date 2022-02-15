import sqlite3
import json

conn = sqlite3.connect('annotations-anonymous.db')

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in tables]

if 'ANNOTATIONS' in tables:
    print('table exists')
    print('are you ABSOLUTELY SURE that you want to DELETE EVERYTHING?')
    choice = input("(y/N): ")
    if not choice == 'y':
        print('not deleting, abort')
        exit()

try:
    conn.execute("DROP TABLE ANNOTATIONS")
    conn.commit()
    print("dropped old table")
except:
    print("no table to drop")


conn.execute('''CREATE TABLE ANNOTATIONS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME NOT NULL,
            SID TEXT NOT NULL,
            ANNOTATION TEXT NOT NULL);''')
print('created table')


conn.commit()


conn.close()
