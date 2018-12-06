import sqlite3
import powerlaw
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

#####
## This is gets powerlaw fit for the full data set.
##
## Run with "python powerlawFull.py"
#####

sqlite_file = './FPA_FOD_20170508.sqlite'

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT FIRE_SIZE FROM fires')
tableData = cur.fetchall()
conn.close()

data = []
minSize = tableData[0][0]
maxSize = tableData[0][0]
for i in range(0, len(tableData)):
    size = tableData[i][0]
    minSize = min(minSize, size)
    maxSize = max(maxSize, size)
    data.append(size)

results = powerlaw.Fit(data[:100])

print("Data Count:", len(data))
print("Min Size Range:", minSize)
print("Max Size Range:", maxSize)
print("alpha:", results.alpha)
print("sigma:", results.sigma)
print("xmin:", results.xmin)
