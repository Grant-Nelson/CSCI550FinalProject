import sqlite3
import pandas as pd
import numpy as np

#################
#
#  This was an attempt to output the data in a way that I could use plot.ly
#  to plot the data with different sized circle sizes. Plot.ly doen't support
#  using a radius so it has to be seperated into channels of data.
#
#################

# Constants
sqlite_file = "FPA_FOD_20170508.sqlite"

latMax = 50.0  # 50 Degrees North
latMin = 25.0  # 25 Degrees North
latRange = latMax-latMin

lonMax = -60.0  # 60 Degrees West
lonMin = -130.0 # 130 Degrees West
lonRange = lonMax-lonMin

width = 1400
height = 800

bucketDiv = 2.0
latBucketNum = int(latRange*bucketDiv)
lonBucketNum = int(lonRange*bucketDiv)

xMinCutoff = 0.0
divisions = 5

# Create buckets for the data
scaledLatBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
scaledLotBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
sizeSumBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
sizeMaxBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
countBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
latBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
lotBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]

# Load wildfire data in to the data array.
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT LATITUDE, LONGITUDE, FIRE_SIZE FROM fires')
data = cur.fetchall()
conn.close()

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
        sizeMaxBuckets[i][j] = max(sizeMaxBuckets[i][j], size)
        countBuckets[i][j] += 1.0

# Get the maximums of each value.
maxCount = 0.0
maxAvgSize = 0.0
maxMaxSize = 0.0
for i in range(latBucketNum):
    for j in range(lonBucketNum):
        count = countBuckets[i][j]
        if count > 0:
            count = countBuckets[i][j]
            size = sizeSumBuckets[i][j]
            avgSize = size / count
            maxSize = sizeMaxBuckets[i][j]

            maxCount = max(maxCount, count)
            maxAvgSize = max(maxAvgSize, avgSize)
            maxMaxSize = max(maxMaxSize, maxSize)

            latBuckets[i][j] = scaledLatBuckets[i][j]/size
            lotBuckets[i][j] = scaledLotBuckets[i][j]/size

# Get data out of buckets and prepare to plot it.
countOutput = "lat-count-0"
for k in range(1, divisions):
    countOutput = "%s, lat-count-%d" % (countOutput, k)

avgSizeOutput = "lat-avgSize-0"
for k in range(1, divisions):
    avgSizeOutput = "%s, lat-avgSize-%d" % (avgSizeOutput, k)

maxSizeOutput = "lat-maxSize-0"
for k in range(1, divisions):
    maxSizeOutput = "%s, lat-maxSize-%d" % (maxSizeOutput, k)

print("latitude, %s, %s, %s" % (countOutput, avgSizeOutput, maxSizeOutput))

countOutput = "%f" % (maxCount/divisions)
for k in range(1, divisions):
    countOutput = "%s, %f" % (countOutput, maxCount*(k+1.0)/divisions)

avgSizeOutput = "%f" % (maxAvgSize/divisions)
for k in range(1, divisions):
    avgSizeOutput = "%s, %f" % (avgSizeOutput, maxAvgSize*(k+1.0)/divisions)

maxSizeOutput = "%f" % (maxMaxSize/divisions)
for k in range(1, divisions):
    maxSizeOutput = "%s, %f" % (maxSizeOutput, maxMaxSize*(k+1.0)/divisions)

print("maximum, %s, %s, %s" % (countOutput, avgSizeOutput, maxSizeOutput))

for i in range(latBucketNum):
    for j in range(lonBucketNum):
        count = countBuckets[i][j]
        if count > 0:
            lat = latBuckets[i][j]
            lon = lotBuckets[i][j]

            countIndex = int(countBuckets[i][j] * divisions/maxCount)
            countIndex = min(countIndex, divisions-1)
            countPick = ["" for k in range(divisions)]
            countPick[countIndex] = "%f" % (lon)
            countOutput = "%s" % (countPick[0])
            for k in range(1, divisions):
                countOutput = "%s, %s" % (countOutput, countPick[k])

            avgSizeIndex = int((sizeSumBuckets[i][j]/count) * divisions/maxAvgSize)
            avgSizeIndex = min(avgSizeIndex, divisions-1)
            avgSizePick = ["" for k in range(divisions)]
            avgSizePick[avgSizeIndex] = "%f" % (lon)
            avgSizeOutput = "%s" % (avgSizePick[0])
            for k in range(1, divisions):
                avgSizeOutput = "%s, %s" % (avgSizeOutput, avgSizePick[k])

            maxSizeIndex = int(sizeMaxBuckets[i][j] * divisions/maxMaxSize)
            maxSizeIndex = min(maxSizeIndex, divisions-1)
            maxSizePick = ["" for k in range(divisions)]
            maxSizePick[maxSizeIndex] = "%f" % (lon)
            maxSizeOutput = "%s" % (maxSizePick[0])
            for k in range(1, divisions):
                maxSizeOutput = "%s, %s" % (maxSizeOutput, maxSizePick[k])

            print("%f, %s, %s, %s" % (lat, countOutput, avgSizeOutput, maxSizeOutput))
