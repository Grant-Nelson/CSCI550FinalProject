import sqlite3
import numpy as np

from mpl_toolkits.basemap import Basemap, cm
from matplotlib.colors import LinearSegmentedColormap

import matplotlib.pyplot as plt

# Collect longitude and latitude for fires
lons = []
lats = []
sqlite_file = './FPA_FOD_20170508.sqlite'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('SELECT LONGITUDE, LATITUDE FROM fires')
data = cur.fetchall()
for entries in data:
    lons.append(entries[0])
    lats.append(entries[1])
conn.close()

# Define the US longitude and latitude
lon_min = -66.0
lon_max = 50.0   ## TODO: These aren't right
lat_min = -125.0  # https://www.kaggle.com/davideanastasia/contour-map-of-us-wildfire-dataset#
lat_max = 24.0

# geographical center of united states
lon_center = -98.583333
lat_center = 39.833333

# Create count of fire bins for the data
lon_bins = np.linspace(lon_max, lon_min, 80)
lat_bins = np.linspace(lat_max, lat_min, 40)
density, _, _ = np.histogram2d(lats, lons, [lat_bins, lon_bins])

# Normalize density
density = np.hstack((density, np.zeros((density.shape[0], 1))))
density = np.vstack((density, np.zeros((density.shape[1]))))

# Create the mesh for the bins
lon_bins_2d, lat_bins_2d = np.meshgrid(lon_bins, lat_bins)


fig = plt.figure(figsize=(12, 8))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
m = Basemap(projection='merc',
            lon_0=lon_bins, lat_0=90., lat_ts=lat_center,
            llcrnrlat=lon_min, urcrnrlat=lon_max,
            llcrnrlon=lat_min, urcrnrlon=lat_max,
            rsphere=6371200., resolution='l', area_thresh=10000)
m.drawcoastlines()
m.drawstates()
m.drawcountries()

CS1 = m.contour(lon_bins_2d, lat_bins_2d, density, 15, linewidths=0.5, colors='k', latlon=True)
CS2 = m.contourf(lon_bins_2d, lat_bins_2d, density, CS1.levels, cmap=plt.cm.PuRd, extend='both', latlon=True)

m.colorbar(CS2)

plt.show()
