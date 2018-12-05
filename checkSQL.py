import sqlite3

#####
## This is basic method for reading from Wildfire database.
##
## Run with "python checkSQL.py"
#####

sqlite_file = './FPA_FOD_20170508.sqlite'

def printData(conn):
    cur = conn.cursor()
    cur.execute('SELECT LATITUDE, LONGITUDE, FIRE_SIZE FROM fires LIMIT 1000')
    data = cur.fetchall()
    for entries in data:
        print(entries[0], entries[1], entries[2])

conn = sqlite3.connect(sqlite_file)
printData(conn)
conn.close()
