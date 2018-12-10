import sqlite3
import pandas as pd
import numpy as np

#################
#
#  This was an attempt to output the data in a way that I could use plot.ly
#  to plot the data with different sized circle sizes. Plot.ly doen't support
#  using a radius so it has to be seperated into channels of data.
#  This one gets the sum of all fire sizes per bucket.
#
#################

# Constants
sqlite_file = "FPA_FOD_20170508.sqlite"
bucketDiv = 2.0
xMinCutoff = 0.0
divisions = 6
maxSizeSum = 840000.0  # 825,498.9

# Load wildfire data in to the data array.
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT LATITUDE, LONGITUDE, FIRE_SIZE FROM fires')
data = cur.fetchall()
conn.close()

# Put all the data into buckets
firstValuesSet = False
latMax = latMin = 0.0
lonMax = lonMin = 0.0
for entries in data:
    size = entries[2]
    if size > xMinCutoff:
        lat = entries[0]
        lon = entries[1]
        if firstValuesSet:
            latMax = max(latMax, lat)
            latMin = min(latMin, lat)
            lonMax = max(lonMax, lon)
            lonMin = min(lonMin, lon)
        else:
            latMax = latMin = lat
            lonMax = lonMin = lon
            firstValuesSet = True

# Create buckets for the data
latRange = latMax-latMin
lonRange = lonMax-lonMin
latBucketNum = int(latRange*bucketDiv)
lonBucketNum = int(lonRange*bucketDiv)
scaledLatBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
scaledLotBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
sizeSumBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
countBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
latBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
lotBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]

# Put all the data into buckets
for entries in data:
    lat = entries[0]
    lon = entries[1]
    size = entries[2]
    if size > xMinCutoff and lat >= latMin and lat <= latMax and lon >= lonMin and lon <= lonMax:
        i = int((lat-latMin)/latRange * (latBucketNum-1))
        j = int((lon-lonMin)/lonRange * (lonBucketNum-1))
        scaledLatBuckets[i][j] += size*lat
        scaledLotBuckets[i][j] += size*lon
        sizeSumBuckets[i][j] += size
        countBuckets[i][j] += 1.0

# Get the maximums of each value.
for i in range(latBucketNum):
    for j in range(lonBucketNum):
        count = countBuckets[i][j]
        if count > 0:
            size = sizeSumBuckets[i][j]
            latBuckets[i][j] = scaledLatBuckets[i][j]/size
            lotBuckets[i][j] = scaledLotBuckets[i][j]/size

# Get data out of buckets and prepare to plot it.
sizeSumOutput = "latitude"
lowValue = 0.0
for k in range(0, divisions):
    highValue = maxSizeSum*(k+1)/divisions
    sizeSumOutput = "%s, [%f-%f)" % (sizeSumOutput, lowValue, highValue)
    lowValue = highValue
print(sizeSumOutput)

for i in range(latBucketNum):
    for j in range(lonBucketNum):
        count = countBuckets[i][j]
        if count > 0:
            lat = latBuckets[i][j]
            lon = lotBuckets[i][j]
            sizeSum = sizeSumBuckets[i][j]

            sizeSumIndex = int(sizeSum * divisions/maxSizeSum)
            sizeSumIndex = min(sizeSumIndex, divisions-1)
            sizeSumPick = ["" for k in range(divisions)]
            sizeSumPick[sizeSumIndex] = "%f" % (lon)
            sizeSumOutput = "%f" % (lat)
            for k in range(0, divisions):
                sizeSumOutput = "%s, %s" % (sizeSumOutput, sizeSumPick[k])
            print(sizeSumOutput)
