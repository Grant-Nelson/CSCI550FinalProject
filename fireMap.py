import sqlite3

#####
## This buckets the sum of fire sizes and count
## based on longitude and latitude from the WildFire data.
## The data is outputted as lon, lat, cumulative size, and count
##
## Run with "python fireMap.py > fireMap.csv"
#####

# Load wildfire data.
sqlite_file = './FPA_FOD_20170508.sqlite'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT LONGITUDE, LATITUDE, FIRE_SIZE FROM fires')
data = cur.fetchall()

# Get the range of the data's lat and lon.
lonMin = data[0][0]
lonMax = data[0][0]
latMin = data[0][1]
latMax = data[0][1]
for entries in data:
    lonMin = min(lonMin, entries[0])
    lonMax = max(lonMax, entries[0])
    latMin = min(latMin, entries[1])
    latMax = max(latMax, entries[1])

lonSize = lonMax-lonMin
latSize = latMax-latMin

# Create buckets for this data.
bucketNo = 1000
sizeBuckets = [[] for i in range(bucketNo)]
countBuckets = [[] for i in range(bucketNo)]

# Collect longitude, latitude, and size of fires bucketted.
def addData(lon, lat, size):
    i = int((lon-lonMin)/lonSize * (bucketNo-1))
    j = int((lat-latMin)/latSize * (bucketNo-1))
    if len(sizeBuckets[i]) <= 0:
        sizeBuckets[i] = [0 for j in range(bucketNo)]
        countBuckets[i] = [0 for j in range(bucketNo)]
    sizeBuckets[i][j] += size
    countBuckets[i][j] += 1

for entries in data:
    addData(entries[0], entries[1], entries[2])

# Print results as csv output.
for i in range(bucketNo):
    for j in range(bucketNo):
        if len(sizeBuckets[i]) > 0:
            count = countBuckets[i][j]
            if count > 0:
                lon = i/(bucketNo-1)*lonSize + lonMin
                lat = j/(bucketNo-1)*latSize + latMin
                size = sizeBuckets[i][j]
                print("%f, %f, %f, %f" % (lon, lat, size, count))
conn.close()
