import sqlite3

#####
## This lists the 10 smallest and 10 largest Wildfires from the data set.
##
## Run with "python checkSQL.py"
#####

sqlite_file = './FPA_FOD_20170508.sqlite'
conn = sqlite3.connect(sqlite_file)

cur1 = conn.cursor()
cur1.execute(
    'SELECT LATITUDE, LONGITUDE, FIRE_YEAR, STATE, FIRE_NAME, FIRE_SIZE ' +
    'FROM fires ' +
    'ORDER BY FIRE_SIZE ASC '
    'LIMIT 10')
data = cur1.fetchall()
print("10 Smallest Fires:")
print(data)

cur2 = conn.cursor()
cur2.execute(
    'SELECT LATITUDE, LONGITUDE, FIRE_YEAR, STATE, FIRE_NAME, FIRE_SIZE ' +
    'FROM fires ' +
    'ORDER BY FIRE_SIZE DESC '
    'LIMIT 10')
data = cur2.fetchall()
print("10 Largest Fires:")
print(data)

conn.close()
