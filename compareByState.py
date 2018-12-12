import sqlite3
import powerlaw
import numpy as np
import math
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
states = []
for tableRow in tableData:
    state = tableRow[1]
    if state not in states:
        states.append(state)
states.sort()

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
    print("   count:", len(data))
    print("   min:", minSize)
    print("   max:", maxSize)

    # Get the powerlaw fit for the current state
    results = powerlaw.Fit(data)
    print("   alpha:", results.alpha)
    print("   sigma:", results.sigma)
    print("   xmin:", results.xmin)

    # Get all the data over the x min result
    overXMinData = []
    for size in data:
        if size > results.xmin:
            overXMinData.append(size)
    print("   overXMin:", len(overXMinData))

    # Compare against other distributions
    # R is the loglikelihood ratio between the two candidate distributions.
    # If R > 0, then the data is more likely to be in the first distribution.
    # If R < 0, then the data is more likely to be in the second distribution.
    # normalized_ratio=True divides R by (sigma*sqrt(n))
    # p is the significance value for the identified direction (i.e., for R > 0 or for R < 0)
    distributions = []
    for dist in results.supported_distributions:
        distributions.append(dist)
    comparisons = []
    for i in range(len(distributions)):
        for j in range(i+1, len(distributions)):
            R, p = results.distribution_compare(distributions[i], distributions[j], normalized_ratio=True)
            if not math.isnan(R):
                if R < 0.0:
                    comparisons.append("   %.6f, %.6f, %s, %s" % (p, -R, distributions[j],  distributions[i]))
                else:   
                    comparisons.append("   %.6f, %.6f, %s, %s" % (p, R, distributions[i], distributions[j]))
    comparisons.sort(reverse=True)
    for i in range(0, min(5, len(comparisons))):
        print(comparisons[i])
    print()
