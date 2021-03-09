#!/usr/bin/python3

import csv
import datetime
import os
import sys

import matplotlib.pyplot as plt


numDays = 14  # Plot (f[date] - f[date - numDays])
maxTicks = 60
plotsDir = "plots"

plotDeaths = "--deaths" in sys.argv
noShow = "--no-show" in sys.argv

toPlot = {
    "Minnesota": ["Carver", "Hennepin", "Ramsey", "Dakota", "Washington", "Scott", "St. Louis"],
    "California": ["Santa Clara", "San Mateo", "Los Angeles", "San Francisco", "San Diego"],
    "Washington": ["King", "Snohomish", "Pierce"],
    "Arizona": ["Maricopa", "Pima", "Pinal", "Gila"]
}


# https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/state/detail/SCPRC-EST2019-18+POP-RES.csv
populationMap = {}
with open("co-est2019-alldata.csv", encoding="latin-1") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=",")
    for row in readCSV:
        if row[6].endswith(" County"):
            row[6] = row[6][:-7]
        populationMap[(row[5], row[6])] = row[18]

# https://www2.census.gov/library/publications/2011/compendia/usa-counties/excel/LND01.xls
areaMap = {}
with open("LND01.csv", encoding="latin-1") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=",")
    curstate = ""
    for row in readCSV:
        if row[0] == "Areaname":
            continue
        if row[0] == "UNITED STATES":
            continue
        if not "," in row[0]:
            curstate = row[0].title()
            areaMap[(curstate, curstate)] = row[3]
            continue
        areaMap[(curstate, row[0].split(",")[0].title())] = row[3]

stateMap = {}
iterator = open("covid-19-data/us-states.csv")
next(iterator)
for line in iterator:
    d = line.split(",")
    state = d[1]
    if not (state in stateMap):
        stateMap[state] = []
    stateMap[state].append((d[0], d[3 + (1 if plotDeaths else 0)]))

countyMap = {}
iterator = open("covid-19-data/us-counties.csv")
next(iterator)
for line in iterator:
    d = line.split(",")
    county = (d[2], d[1])
    if not (county in countyMap):
        countyMap[county] = []
    countyMap[county].append((d[0], d[4 + (1 if plotDeaths else 0)]))

for state in toPlot:
    fig = plt.figure(figsize=(24, 12))
    counties = toPlot[state]

    stateCaseCounts = stateMap[state]
    x = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in stateCaseCounts]
    y = [int(i[1]) * 100 / float(populationMap[(state, state)]) for i in stateCaseCounts]
    y = [y[i] - y[max(0, i - numDays)] for i in range(0, len(y))]

    plt.locator_params(axis="y", nbins=25)

    tickIdc = range(0, len(x), len(x) // maxTicks + 1)
    plt.xticks([x[i] for i in tickIdc], [[i[0] for i in stateCaseCounts][j] for j in tickIdc], rotation=90)
    plt.plot(x, y, marker="o", color="k", label=state)

    i = 0
    for county in counties:
        countyCaseCounts = countyMap[(state, county)]
        x = [datetime.datetime.strptime(i[0], "%Y-%m-%d").date() for i in countyCaseCounts]
        y = [int(i[1]) * 100 / float(populationMap[(state, county)]) for i in countyCaseCounts]
        y = [y[i] - y[max(0, i - numDays)] for i in range(0, len(y))]
        plt.plot(x, y, marker="o", color="C%s" % i, label=county)
        i = i + 1

    plt.legend(loc="upper left")
    plt.grid(axis="both")
    plt.ylim(bottom=0)
    plt.title(state + " % of the population with new COVID-19 " + ("deaths" if plotDeaths else "cases")
              + " in past " + str(numDays) + " days. Data from NYT "
                                             "https://github.com/nytimes/covid-19-data and US census. By Evan "
                                             "Severson")
    if noShow:  # might remove this condition check
        if not os.path.exists(plotsDir):
            os.mkdir(plotsDir)
        fig.savefig(plotsDir + "/" + state + ("-deaths" if plotDeaths else "") + ".png", dpi=200)

if not noShow:
    plt.show()
