import sqlite3
import powerlaw
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

#####
## This is gets powerlaw fit per year for the full data set.
##
## Run with "python powerlawByYear.py > byYear.csv"
#####

sqlite_file = './FPA_FOD_20170508.sqlite'

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT FIRE_SIZE, FIRE_YEAR FROM fires')
tableData = cur.fetchall()
conn.close()

years = {}
for i in range(0, len(tableData)):
    years[tableData[i][1]] = True

print("year, count, overXMin, min, max, alpha, sigma, xmin")

for year in years:
    data = []
    minSize = tableData[0][0]
    maxSize = tableData[0][0]
    for i in range(0, len(tableData)):
        if tableData[i][1] == year:
            size = tableData[i][0]
            minSize = min(minSize, size)
            maxSize = max(maxSize, size)
            data.append(size)

    results = powerlaw.Fit(data)

    overXMin = 0
    for i in range(0, len(data)):
        if data[i] > results.xmin:
            overXMin += 1

    print(year, ",", len(data), ",", overXMin, ",", minSize,
          ",",  maxSize, ",",  results.alpha,
          ",",results.sigma, ",",  results.xmin)
