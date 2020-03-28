import datetime
import urllib.request

import matplotlib.pyplot as plt

stateMap = {}
iterator = iter(urllib.request.urlopen("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"))
next(iterator)
for line in iterator:
    d = line.decode('utf-8').split(",")
    state = d[1]
    if not (state in stateMap):
        stateMap[state] = []
    stateMap[state].append((d[0], d[3]))

countyMap = {}
iterator = iter(urllib.request.urlopen("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"))
next(iterator)
for line in iterator:
    d = line.decode('utf-8').split(",")
    county = (d[2], d[1])
    if not (county in countyMap):
        countyMap[county] = []
    countyMap[county].append((d[0], d[4]))

state = "Minnesota"
counties = ["Carver", "Hennepin", "Ramsey", "Dakota", "Washington"]

# state = "California"
# counties = ["Santa Clara", "San Mateo", "Los Angeles", "San Francisco", "San Diego"]

# state = "Washington"
# counties = ["King", "Snohomish", "Pierce"]

# plot state
stateCaseCounts = stateMap[state]
x = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in stateCaseCounts]
y = [int(i[1]) for i in stateCaseCounts]

plt.locator_params(axis="y", nbins=25)

plt.xticks(x, [i[0] for i in stateCaseCounts], rotation=90)
plt.plot(x, y, marker="o", color="k", label=state)

i = 0
for county in counties:
    countyCaseCounts = countyMap[(state, county)]
    x = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in countyCaseCounts]
    y = [int(i[1]) for i in countyCaseCounts]
    plt.plot(x, y, marker="o", color="C%s" % i, label=county)
    i = i + 1


plt.legend(loc="upper left")
plt.grid(axis="both")
plt.ylim(bottom=0)
plt.title(state + " Covid 19 case trend. Data from NYT https://github.com/nytimes/covid-19-data. By Evan Severson")

plt.show()