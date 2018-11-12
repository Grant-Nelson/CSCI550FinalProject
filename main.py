import sqlite3

def printTitleNames(cur):
    cur.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    tableNames = cur.fetchall()
    print("Table Names:")
    for name in tableNames:
        print('   ', name[0])

sqlite_file = './FPA_FOD_20170508.sqlite'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

printTitleNames(cur)

conn.close()
