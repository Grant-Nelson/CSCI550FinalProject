import sqlite3

#####
## This buckets the sum of fire sizes and count
## based on latitude and longitude from the WildFire data.
## The data is outputted as lat, lon, cumulative size, and count.
## Remove the stats off the top of the file before importing it.
##
## Run with "python fireMap.py > fireMap.csv"
#####

bucketScalar = 2.0 # Number of buckets divisions per lon and lat
countThreshold = 1000 # Must be 1 or more

# Load wildfire data.
sqlite_file = './FPA_FOD_20170508.sqlite'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT LONGITUDE, LATITUDE, FIRE_SIZE FROM fires')
data = cur.fetchall()

# Get the range of the data's lat and lon.
latMin = data[0][1]
latMax = data[0][1]
lonMin = data[0][0]
lonMax = data[0][0]
for entries in data:
    latMin = min(latMin, entries[1])
    latMax = max(latMax, entries[1])
    lonMin = min(lonMin, entries[0])
    lonMax = max(lonMax, entries[0])

latSize = latMax-latMin
lonSize = lonMax-lonMin
latBucketNo = int(latSize*bucketScalar+1)
lonBucketNo = int(lonSize*bucketScalar+1)

# Create buckets for this data.
sizeSumBuckets = [[] for i in range(latBucketNo)]
countBuckets = [[] for i in range(latBucketNo)]

# Collect longitude, latitude, and size of fires bucketted.
def addData(lon, lat, size):
    i = int((lat-latMin)/latSize * (latBucketNo-1))
    j = int((lon-lonMin)/lonSize * (lonBucketNo-1))
    if len(sizeSumBuckets[i]) <= 0:
        sizeSumBuckets[i] = [0 for j in range(lonBucketNo)]
        countBuckets[i] = [0 for j in range(lonBucketNo)]
    sizeSumBuckets[i][j] += size
    countBuckets[i][j] += 1

for entries in data:
    addData(entries[0], entries[1], entries[2])
conn.close()

# Collect the maximum values from the buckets.
maxSizeSum = 0.0
maxSizeAvg = 0.0
maxCount = 0
for i in range(latBucketNo):
    for j in range(lonBucketNo):
        if len(sizeSumBuckets[i]) > 0:
            count = countBuckets[i][j]
            if count > 0:
                sizeSum = sizeSumBuckets[i][j]
                maxSizeSum = max(maxSizeSum, sizeSum)
                maxSizeAvg = max(maxSizeAvg, sizeSum/count)
                maxCount = max(maxCount, count)

# Print some stats about data.
print("lat range: %f to %f (%f)" % (latMin, latMax, latSize))
print("lon range: %f to %f (%f)" % (lonMin, lonMax, lonSize))
print("buckets dim: %d, %d" % (latBucketNo, lonBucketNo))
print("buckets range: %f, %f" % (latSize/latBucketNo, lonSize/lonBucketNo))
print("max size: sum: %f, avg %f" % (maxSizeSum, maxSizeAvg))
print("max count: %d" % (maxCount))

# Print results as csv output.
for i in range(latBucketNo):
    for j in range(lonBucketNo):
        if len(sizeSumBuckets[i]) > 0:
            count = countBuckets[i][j]
            if count >= countThreshold:
                lat = i/(latBucketNo-1)*latSize + latMin
                lon = j/(lonBucketNo-1)*lonSize + lonMin
                size = sizeSumBuckets[i][j]
                print("%f, %f, %f, %d" % (lat, lon, size, count))
