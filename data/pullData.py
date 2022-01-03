import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
                 parse_dates=["date"])
# df = df[df["location"] == "World"]
keep = ["location", "date", "total_cases", "new_cases", "icu_patients", "new_deaths", "hosp_patients", "new_tests",
        "new_vaccinations", "people_vaccinated", "people_fully_vaccinated", "total_boosters", "iso_code"]
df = df[keep]

def process_pandemic_data(df):
    location = [x for x in df['location'].unique().tolist()
                if type(x) == str]
    #print(location)
    latitude = []
    longitude = []
    for i in range(0, len(location)):
        # remove things that does not seem usefull here
        try:
            address = location[i]
            geolocator = Nominatim(user_agent="ny_explorer")
            loc = geolocator.geocode(address)
            #print(address)
            #print(loc.latitude)
            #print(loc.longitude)
            latitude.append(loc.latitude)
            longitude.append(loc.longitude)
            #print('The geographical coordinate of location are {}, {}.'.format(loc.latitude, loc.longitude))
        except:
            # in the case the geolocator does not work, then add nan element to list
            # to keep the right size
            latitude.append(np.nan)
            longitude.append(np.nan)
    # create a dataframe with the locatio, latitude and longitude
    df_ = pd.DataFrame({'location': location,
                        'latitude': latitude,
                        'longitude': longitude})
    # merge on Restaurant_Location with rest_df to get the column
    new_df = df.merge(df_, on='location', how='left')

    print(new_df.head(10))

    return new_df

df = process_pandemic_data(df)

df.to_csv("data/owid-dataset.csv")
print(df.head())
