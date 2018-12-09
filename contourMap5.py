import sqlite3
import pandas as pd
import numpy as np

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

bucketDiv = 10.0
latBucketNum = int(latRange*bucketDiv)
lonBucketNum = int(lonRange*bucketDiv)

xMinCutoff = 234.0

# Create buckets for the data
sizeSumBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
sizeMaxBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
countBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]

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
        sizeSumBuckets[i][j] += size
        sizeMaxBuckets[i][j] = max(sizeMaxBuckets[i][j], size)
        countBuckets[i][j] += 1.0

# Get data out of buckets and prepare to plot it.
print("latitude, longitude, count, avgSize, maxSize")
for i in range(latBucketNum):
    for j in range(lonBucketNum):
        count = countBuckets[i][j]
        if count > 0:
            lat = i/float(latBucketNum-1) * latRange + latMin
            lon = j/float(lonBucketNum-1) * lonRange + lonMin

            count = countBuckets[i][j]
            avgSize = sizeSumBuckets[i][j] / count
            maxSize = sizeMaxBuckets[i][j]

            print("%f, %f, %f, %f, %f" % (lat, lon, count, avgSize, maxSize))
