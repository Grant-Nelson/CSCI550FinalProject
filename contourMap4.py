import sqlite3
import pandas as pd
import numpy as np
import colorcet as cc
from bokeh.plotting import figure, output_file, show

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

latBucketNum = int(latRange*10.0)
lonBucketNum = int(lonRange*10.0)

# Create buckets for the data
sizeMaxBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
countBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]

# Load wildfire data in to the data array.
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT LATITUDE, LONGITUDE, FIRE_SIZE FROM fires')
data = cur.fetchall()
conn.close()

# Put all the data into buckets
maxSize = 0.0
maxCount = 0.0
for entries in data:
    lat = entries[0]
    lon = entries[1]
    size = entries[2]
    if size > 234.0 and lat >= latMin and lat <= latMax and lon >= lonMin and lon <= lonMax:
        i = int((lat-latMin)/latRange * (latBucketNum-1))
        j = int((lon-lonMin)/lonRange * (lonBucketNum-1))
        sizeMaxBuckets[i][j] = max(sizeMaxBuckets[i][j], size)
        countBuckets[i][j] += 1.0
        maxSize = max(maxSize, size)
        maxCount = max(maxCount, countBuckets[i][j])

# Get data out of buckets and prepare to plot it.
latResults = []
lonResults = []
sizeValues = []
colorResults = []
radiusResult = []
for i in range(latBucketNum):
    for j in range(lonBucketNum):
        size = sizeMaxBuckets[i][j]
        if size > 234.0:
            lat = i/float(latBucketNum-1) * latRange + latMin
            lon = j/float(lonBucketNum-1) * lonRange + lonMin
            value = pow(size/maxSize, 0.5)
            color = cc.fire[int(value * (len(cc.fire)-1))]
            radius = countBuckets[i][j]*0.5/maxCount+0.2
            
            latResults.append(lat)
            lonResults.append(lon)
            sizeValues.append(size)
            colorResults.append(color)
            radiusResult.append(radius)

# Sort the output by size
def swap(list, i, j):
    value = list[i]
    list[i] = list[j]
    list[j] = value

for i in range(0, len(sizeValues)):
    minValue = sizeValues[i]
    indexOfMin = i
    for j in range(i+1, len(sizeValues)):
        if minValue > sizeValues[j]:
            minValue = sizeValues[j]
            indexOfMin = j
    swap(latResults, i, indexOfMin)
    swap(lonResults, i, indexOfMin)
    swap(sizeValues, i, indexOfMin)
    swap(colorResults, i, indexOfMin)
    swap(radiusResult, i, indexOfMin)

# Plot
output_file("plot.html", title="fire maximum size", mode="cdn")

TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
p = figure(tools=TOOLS, x_range=(lonMin, lonMax), y_range=(latMin, latMax),
           width=width, height=height, background_fill_color="#000000")
p.grid.grid_line_color = None
p.circle(lonResults, latResults, radius=radiusResult, fill_color=colorResults, line_color=None)

show(p)
