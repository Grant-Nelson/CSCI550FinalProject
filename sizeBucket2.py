import sqlite3
import math

#####
## This log-buckets the fire sizes.
## The data is outputted as size, count, log size, and log count.
##
## Run with "python sizeBucket.py > sizeBucket.csv"
#####

bucketCount = 1000

# Load wildfire data.
sqlite_file = './FPA_FOD_20170508.sqlite'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT FIRE_SIZE FROM fires')
data = cur.fetchall()

# Get the range of the data.
minSize = float(data[0][0])
maxSize = float(data[0][0])
for entries in data:
    size = entries[0]
    minSize = min(minSize, size)
    maxSize = max(maxSize, size)
sizeRange = maxSize-minSize

# Create buckets for this data.
sizeBuckets = [0.0 for i in range(bucketCount)]
countBuckets = [0.0 for i in range(bucketCount)]

# Collect size of fires bucketted.
for entries in data:
    size = entries[0]
    i = int((size-minSize)/sizeRange * (bucketCount-1))
    sizeBuckets[i] += size
    countBuckets[i] += 1.0
conn.close()

print("max: %f" % maxSize)
print("min: %f" % minSize)

# Print results as csv output.
for i in range(bucketCount):
    count = countBuckets[i]
    if count > 0:
        sizeAvg = sizeBuckets[i]/count
        logCount = math.log(count)
        logSize = 0 if size <= 0 else math.log(size)
        print("%f, %f, %f, %f" % (size, count, logSize, logCount))
