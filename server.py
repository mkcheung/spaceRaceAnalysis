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
spaceRaceDf = pd.read_csv(f"{workingDirectory}/mission_launches.csv")

# shape of the spaceRaceDf
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


cntrLnchByYr = spaceRaceDf.groupby(['Year', 'Country']).size().reset_index(name='Launches');
cntrWMostLnchsByYr = cntrLnchByYr.loc[cntrLnchByYr.groupby('Year')['Launches'].idxmax()]

cntrWMostLnchsByYr_pivot = cntrWMostLnchsByYr.pivot(
    index='Country',
    columns='Year',
    values='Launches'
).fillna(0)
plt.figure(figsize=(20, 6), constrained_layout=True)
plt.imshow(cntrWMostLnchsByYr_pivot, aspect='auto')
plt.yticks(range(len(cntrWMostLnchsByYr_pivot.index)), cntrWMostLnchsByYr_pivot.index)
plt.xticks(range(len(cntrWMostLnchsByYr_pivot.columns)), cntrWMostLnchsByYr_pivot.columns, rotation=45)
plt.colorbar(label='Launches')
plt.title('Launches per Country per Year')
plt.xlabel('Year')
plt.ylabel('Country')
plt.show()
