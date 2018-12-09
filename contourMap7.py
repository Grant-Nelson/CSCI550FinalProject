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
divisions = 6
maxMaxSize = 600000.0

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
for i in range(latBucketNum):
    for j in range(lonBucketNum):
        count = countBuckets[i][j]
        if count > 0:
            size = sizeSumBuckets[i][j]
            latBuckets[i][j] = scaledLatBuckets[i][j]/size
            lotBuckets[i][j] = scaledLotBuckets[i][j]/size

# Get data out of buckets and prepare to plot it.
maxSizeOutput = "lat-maxSize-0"
for k in range(1, divisions):
    maxSizeOutput = "%s, lat-maxSize-%d" % (maxSizeOutput, k)

print("latitude, %s" % (maxSizeOutput))

for i in range(latBucketNum):
    for j in range(lonBucketNum):
        count = countBuckets[i][j]
        if count > 0:
            lat = latBuckets[i][j]
            lon = lotBuckets[i][j]

            maxSizeIndex = int(sizeMaxBuckets[i][j] * divisions/maxMaxSize)
            maxSizeIndex = min(maxSizeIndex, divisions-1)
            maxSizePick = ["" for k in range(divisions)]
            maxSizePick[maxSizeIndex] = "%f" % (lon)
            maxSizeOutput = "%s" % (maxSizePick[0])
            for k in range(1, divisions):
                maxSizeOutput = "%s, %s" % (maxSizeOutput, maxSizePick[k])

            print("%f, %s" % (lat, maxSizeOutput))
