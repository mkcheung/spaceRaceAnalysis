import json
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.dates as mdates
from SPARQLWrapper import SPARQLWrapper, JSON

ambiguousSiteCountries = {
    'Barents Sea': 'Russia',
    'Gran Canaria': 'Space',
    'Pacific Missile Range Facility': 'USA',
    'Shahrud Missile Test Site': 'Iran',
    'Yellow Sea': 'China'
}

workingDirectory = Path(__name__).resolve().parent
print(workingDirectory)
spaceRaceDf = pd.read_csv(f"{workingDirectory}/mission_launches.csv")

# shape of the spaceRaceDf
print(spaceRaceDf.shape)
print(spaceRaceDf.info())
print(spaceRaceDf[['Date', 'Location']])
format_str = '%a %b %d, %Y %H:%M %Z'
spaceRaceDf["Date"] = pd.to_datetime(spaceRaceDf['Date'], format=format_str, errors="coerce", utc=True)

def extractCountry(location):
    locComponents = location.split(",")
    countryIndex = len(locComponents)-1;
    return locComponents[countryIndex].strip()

spaceRaceDf["Country"] = spaceRaceDf["Location"].apply(extractCountry)
mappedValues = spaceRaceDf['Country'].map(ambiguousSiteCountries)
spaceRaceDf['Country'] = mappedValues.fillna(spaceRaceDf['Country'])
spaceRaceDf["Year"] = spaceRaceDf['Date'].dt.year.astype("Int64")


cntrLaunchesByYr = spaceRaceDf.groupby(['Year', 'Country']).agg({'Location':'count'});

# get the year and country out of the multiindex with the row having the most launches
yrCountryMostLnchDf = cntrLaunchesByYr.groupby('Year')['Location'].idxmax()

cntrMostLaunchesByYr = cntrLaunchesByYr.loc[yrCountryMostLnchDf.values]
print(cntrMostLaunchesByYr)
cntrMostLaunSeries = cntrMostLaunchesByYr['Location'].squeeze()
print(cntrMostLaunchesByYr['Location'].squeeze())
print(type(cntrMostLaunchesByYr['Location'].squeeze()))
countries = cntrMostLaunchesByYr.index.get_level_values('Country')
colorMap = {
    'USA': 'tab:blue',
    'Russia': 'tab:red',
    'Kazakhstan': 'tab:green',
    'China': 'tab:orange',
    'Japan': 'tab:purple',
    'New Zealand': 'tab:brown'
}
barColors = [colorMap[c] for c in countries]
# plot by series so bars can be set by color
cntrMostLaunSeries.plot(
    kind="bar",
    figsize=(14, 6),
    color=barColors
)
plt.tight_layout()
plt.show()
