import sqlite3
import powerlaw
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

#####
## This is a test bed for running powerlaw fit.
##
## Run with "python powerlaw1.py"
#####

sqlite_file = './FPA_FOD_20170508.sqlite'

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT FIRE_SIZE, STATE FROM fires')
tableData = cur.fetchall()
conn.close()

print("Original Data Count: %d" % (len(tableData)))

#data = [tableData[i][0] for i in range(0, len(tableData))]
data = []
minSize = 1.0e12
maxSize = -1.0e12
for i in range(0, len(tableData)):
    size = tableData[i][0]
    minSize = min(minSize, size)
    maxSize = max(maxSize, size)
    data.append(size)

print("Data Count: %d" %(len(data)))
print("Size Range: %f..%f" %(minSize, maxSize))

results = powerlaw.Fit(data[:100])
print("alpha:", results.alpha)
print("sigma:", results.sigma)
print("xmax:", results.xmax)
