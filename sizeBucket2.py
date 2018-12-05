import sqlite3
import math

#####
## This log-buckets the fire sizes.
## The data is outputted as size, count, log size, and log count.
##
## Run with "python sizeBucket2.py > sizeBucket2.csv"
#####

bucketCount = 10000

# Load wildfire data.
sqlite_file = './FPA_FOD_20170508.sqlite'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT FIRE_SIZE FROM fires')
data = cur.fetchall()

# Gets the log bin value
def logBin(size):
    return math.pow(2.0, math.floor(math.log2(size)))

# Get the range of the data.
minSize = float(data[0][0])
maxSize = float(data[0][0])
for entries in data:
    size = entries[0]
    minSize = min(minSize, size)
    maxSize = max(maxSize, size)

minBucketSize = logBin(minSize)
maxBucketSize = logBin(maxSize)
bucketSizeRange = maxBucketSize-minBucketSize

# Create buckets for this data.
sizeSumBuckets = [0.0 for i in range(bucketCount)]
sizeMinBuckets = [maxSize for i in range(bucketCount)]
sizeMaxBuckets = [0.0 for i in range(bucketCount)]
countBuckets = [0.0 for i in range(bucketCount)]

# Collect size of fires bucketted.
for entries in data:
    size = entries[0]
    i = int((logBin(size)-minBucketSize)/bucketSizeRange * (bucketCount-1))
    sizeSumBuckets[i] += size
    sizeMinBuckets[i] = min(sizeMinBuckets[i], size)
    sizeMaxBuckets[i] = max(sizeMaxBuckets[i], size)
    countBuckets[i] += 1.0
conn.close()

# Print results as csv output.
for i in range(bucketCount):
    count = countBuckets[i]
    if count > 0:
        sizeAvg = sizeSumBuckets[i]/count
        sizeMin = sizeMinBuckets[i]
        sizeMax = sizeMaxBuckets[i]
        logCount = math.log(count)
        logSize = 0 if sizeAvg <= 0 else math.log(sizeAvg)
        print("%d, " % (i) +
                "%f, %f, %f, " % (sizeAvg, sizeMin, sizeMax) +
                "%d, %f, %f" % (count, logSize, logCount))
