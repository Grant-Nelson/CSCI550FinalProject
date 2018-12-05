import sqlite3
import powerlaw

#####
## This is
##
## Run with "python powerlaw1.py"
#####

sqlite_file = './FPA_FOD_20170508.sqlite'

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT FIRE_SIZE FROM fires')
tableData = cur.fetchall()
conn.close()

data = [tableData[i][0] for i in range(0, len(tableData))]

results = powerlaw.Fit(data)
print(results)
