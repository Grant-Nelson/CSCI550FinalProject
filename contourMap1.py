import sqlite3
import pandas as pd
import numpy as np
import colorcet as cc
from bokeh.plotting import figure, output_file, show

# Constants
sqlite_file = "FPA_FOD_20170508.sqlite"

latMax = 50.0  # 50° North
latMin = 25.0  # 25° North
latRange = latMax-latMin

lonMax = -60.0  # 60° West
lonMin = -130.0 # 130° West
lonRange = lonMax-lonMin

width = 1400
height = 800

latBucketNum = int(latRange*4.0)
lonBucketNum = int(lonRange*4.0)

radiiMax = 2.0
radiiMin = 0.0
radiiRange = radiiMax - radiiMin

# Create buckets for the data
sizeSumBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
countBuckets = [[0 for j in range(lonBucketNum)] for i in range(latBucketNum)]
sizeAvgBuckets = [[0.0 for j in range(lonBucketNum)] for i in range(latBucketNum)]

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
    if lat >= latMin and lat <= latMax and lon >= lonMin and lon <= lonMax:
        i = int((lat-latMin)/latRange * (latBucketNum-1))
        j = int((lon-lonMin)/lonRange * (lonBucketNum-1))
        sizeSumBuckets[i][j] += size
        countBuckets[i][j] += 1

# Get maximum size of fire average for the buckets
maxSizeAvg = 0.0
for i in range(latBucketNum):
    for j in range(lonBucketNum):
        count = countBuckets[i][j]
        if count > 0:
            sizeAvg = sizeSumBuckets[i][j]/count
            sizeAvgBuckets[i][j] = sizeAvg
            maxSizeAvg = max(maxSizeAvg, sizeAvg)

# Get data out of buckets and prepare to plot it.
latResults = []
lonResults = []
radiiResults = []
for i in range(latBucketNum):
    for j in range(lonBucketNum):
        sizeAvg = sizeAvgBuckets[i][j]
        if sizeAvg > 0.0:
            lat = i/float(latBucketNum-1) * latRange + latMin
            lon = j/float(lonBucketNum-1) * lonRange + lonMin
            radii = pow(sizeAvg/maxSizeAvg, 0.5) * radiiRange + radiiMin
            
            latResults.append(lat)
            lonResults.append(lon)
            radiiResults.append(radii)

# Plot
output_file("plot.html", title="fire size average", mode="cdn")

TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
p = figure(tools=TOOLS, x_range=(lonMin, lonMax), y_range=(latMin, latMax), width=width, height=height)
p.circle(lonResults, latResults, radius=radiiResults, fill_color="#000000", fill_alpha=0.4, line_color=None)

show(p)
 