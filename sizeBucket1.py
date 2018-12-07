import sqlite3
import math

#####
## This buckets the fire sizes.
##
## Run with "python sizeBucket1.py > sizeBucket1.csv"
#####

bucketCount = 1000

# Load wildfire data.
sqlite_file = './FPA_FOD_20170508.sqlite'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT FIRE_SIZE FROM fires')
data = cur.fetchall()
conn.close()

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

# Collect size of fires bucketted.
for entries in data:
    size = entries[0]
    i = int((size-minSize)/sizeRange * (bucketCount-1))
    sizeBuckets[i] += 1.0

# Print results as csv output.
print("size, count, logSize, logCount")
for i in range(bucketCount):
    count = sizeBuckets[i]
    if count > 0:
        size = i/(bucketCount-1)*sizeRange + minSize
        logCount = math.log(count)
        logSize = 0 if size <= 0 else math.log(size)
        print("%f, %f, %f, %f" % (size, count, logSize, logCount))
