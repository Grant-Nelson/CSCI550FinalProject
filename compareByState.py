import sqlite3
import powerlaw
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

# Constants
sqlite3_filename = "FPA_FOD_20170508.sqlite"

# Get data out of data base
conn = sqlite3.connect(sqlite3_filename)
cur = conn.cursor()
cur.execute('SELECT FIRE_SIZE, STATE FROM fires')
tableData = cur.fetchall()
conn.close()

# Collect a list of all state abbreviations
states = {}
for tableRow in tableData:
    states[tableRow[1]] = True

for state in states:
    print("state:", state)

    # Collect all the data for the current state
    data = []
    minSize = maxSize = tableData[0][0]
    for tableRow in tableData:
        if tableRow[1] == state:
            size = tableRow[0]
            minSize = min(minSize, size)
            maxSize = max(maxSize, size)
            data.append(size)
    print("count:", len(data))
    print("min:", minSize)
    print("max:", maxSize)

    # Get the powerlaw fit for the current state
    results = powerlaw.Fit(data)
    print("alpha:", results.alpha)
    print("sigma:", results.sigma)
    print("xmin:", results.xmin)

    # Get all the data over the x min result
    overXMinData = []
    for size in data:
        if size > results.xmin:
            overXMinData.append(size)
    print("overXMin:", len(overXMinData))

    # Compare against other distributions
    # R is the loglikelihood ratio between the two candidate distributions.
    # If R > 0, then the data is more likely to be in the first distribution.
    # If R < 0, then the data is more likely to be in the second distribution.
    # normalized_ratio=True divides R by (sigma*sqrt(n))
    # p is the significance value for the identified direction (i.e., for R > 0 or for R < 0)
    distributions = results.supported_distributions
    for firstDist in distributions:
        for secondDist in distributions:
            R, p = results.distribution_compare(firstDist, secondDist, normalized_ratio=True)
            print(firstDist, "<?>", secondDist)
            print("   R:", R, "=>", (firstDist if R > 0 else secondDist))
            print("   p:", p)
