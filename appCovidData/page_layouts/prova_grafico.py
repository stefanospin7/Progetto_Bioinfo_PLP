import pandas as pd
import numpy as np
import plotly.graph_objects as go
from geopy.geocoders import Nominatim

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# Define dataset path
dataset = "data/owid-dataset.csv"

# Load dataset
df = pd.read_csv(dataset)

# Display first 5 lines
df.head()


def process_pandemic_data(df):
    # Columns renaming
    df.columns = [col.lower() for col in df.columns]


    # Pivoting per category
    # df = pd.pivot_table(df, values='count', index=['date', 'zone'], columns=['category'])
    # df.columns = ['confirmed', 'deaths', 'recovered']

    # Merging locations after pivoting
    # df = df.join(country_position)

    # Filling nan values with 0
    df = df.fillna(0)

    # Compute bubble sizes
    df['sizeTC'] = df['total_cases'].apply(lambda x: (np.sqrt(x / 100) + 1) if x > 500 else (np.log(x) / 2 + 1)).replace(
        np.NINF, 0)
    df['sizeND'] = df['new_deaths'].apply(
        lambda x: (np.sqrt(x / 100) + 1) if x > 500 else (np.log(x) / 2 + 1)).replace(
        np.NINF, 0)

    # Compute bubble color
    df['colorTC'] = (df['new_cases'] / df['total_cases']).fillna(0).replace(np.inf, 0)
    df['colorND'] = (df['new_deaths'] / df['total_cases']).fillna(0).replace(np.inf, 0)

    location = [x for x in df['iso_code'].unique().tolist()
                if type(x) == str]
    latitude = []
    longitude = []
    for i in range(0, len(location)):
        # remove things that does not seem usefull here
        try:
            address = location[i]
            geolocator = Nominatim(user_agent="ny_explorer")
            loc = geolocator.geocode(address)
            latitude.append(loc.latitude)
            longitude.append(loc.longitude)
            #print('The geographical coordinate of location are {}, {}.'.format(loc.latitude, loc.longitude))
        except:
            # in the case the geolocator does not work, then add nan element to list
            # to keep the right size
            latitude.append(np.nan)
            longitude.append(np.nan)
    # create a dataframe with the locatio, latitude and longitude
    df_ = pd.DataFrame({'iso_code': location,
                        'latitude': latitude,
                        'longitude': longitude})
    # merge on Restaurant_Location with rest_df to get the column
    new_df = df.merge(df_, on='iso_code', how='left')

    print(new_df.head(10))

    return new_df

df = process_pandemic_data(df)

#df.set_index(['date'], inplace=True)
#df.sort_values("iso_code", axis=0)

#df_iso = pd.read_csv('https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv')

#df_iso.rename(columns={df_iso.columns[2]:'iso_code'}, inplace=True)
#df_iso['iso_code'] = df_iso['iso_code'].astype('str')
#df['iso_code'] = df['iso_code'].astype('str')
#print(df_iso.head(5))

#frames = [df, df_iso]
#result = pd.merge(df, df_iso, how="cross")
#result = pd.concat(frames, keys=df.iso_code)

#dfC = pd.merge(df, df_iso, on="iso_code", how="outer")
#dfC = pd.concat([df, df_iso], axis=0, ignore_index=True, join="inner")
#print(dfC.head(5))

# Selecting the day to display
day = '2020-03-08'
#tmp = df[df["date"] == day]
#print(tmp.head(10))
#tmp = df.xs(day)


dati_covid = ["sizeTC", "sizeND"]
colori_covid = ["colorTC","colorND"]
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]

# # Create the figure and feed it all the prepared columns
# fig = go.Figure()
#
# for i in range(len(dati_covid)):
#     #lim = dati_covid[i]
#     fig.add_trace(
#         go.Scattermapbox(
#             lat=tmp["latitude"],
#             lon=tmp["longitude"],
#             # locations=tmp['iso_code'],
#             mode='markers',
#             marker=go.scattermapbox.Marker(
#                 size=tmp[dati_covid[i]],
#                 color=tmp[colori_covid[i]]
#             )
#         ),
#         #name = '{0} - {1}'.format(lim[0],lim[1]))
#     )



days = df.date.tolist()


dataM = [],

def generate_marker(i, n, day):
    mark = go.scattermapbox.Marker(
                size=df[df["date"] == day][i],
                color=df[df["date"] == day][n],
                #    showscale=True,
                #    colorbar={'title':'Recovered', 'titleside':'top', 'thickness':4, 'ticksuffix':' %'},
            )
    return mark

def generate_frame(day):
    marcatori = []
    for i in range(len(dati_covid)):
        marcatori.append(generate_marker(dati_covid[i], colori_covid[i], day))

    frame = {
        'name': 'frame_{}'.format(day),
        'data': {
            'type': 'scattermapbox',
            'lat': df[df["date"] == day]['latitude'],
            'lon': df[df["date"] == day]['longitude'],
            'marker': {go.scattermapbox.Marker(
                size=df[df["date"] == day][i],
                color=df[df["date"] == day][n],
                #    showscale=True,
                #    colorbar={'title':'Recovered', 'titleside':'top', 'thickness':4, 'ticksuffix':' %'},
            )},
            # 'customdata':np.stack((df.xs(day)['confirmed_display'], df.xs(day)['recovered_display'],  df.xs(day)['deaths_display'], pd.Series(df.xs(day).index)), axis=-1),
            # 'hovertemplate': "<extra></extra><em>%{customdata[3]}  </em><br>🚨  %{customdata[0]}<br>🏡  %{customdata[1]}<br>⚰️  %{customdata[2]}",
        }
    }
    return frame

days = ["2021-12-01", "2021-12-02"]

frames = []
for day in days:
    frames.append(generate_frame(day))




sliders = [{
    'transition':{'duration': 0},
    'x':0.08,
    'len':0.88,
    'currentvalue':{'font':{'size':15}, 'prefix':'📅 ', 'visible':True, 'xanchor':'center'},
    'steps':[
        {
            'label':day,
            'method':'animate',
            'args':[
                ['frame_{}'.format(day)],
                {'mode':'immediate', 'frame':{'duration':100, 'redraw': True}, 'transition':{'duration':50}}
              ],
        } for day in days]
}]


# Defining the initial state
data = frames[0]['data']

# Adding all sliders and play button to the layout
layout = go.Layout(
    sliders=sliders,
    #updatemenus=play_button,
    mapbox={
        'accesstoken':"pk.eyJ1IjoibWFuZnJlZG9mcmFjY29sYSIsImEiOiJja3hyd2JjbnEwNnVjMnBvNTZrbHBqdmwzIn0.YFYLdLUxoYC3gSpkcGplqQ",
        'center':{"lat": 37.86, "lon": 2.15},
        'zoom':1.7,
        'style':'light',
    }
)

# Creating the figure
fig = go.Figure(data=data, layout=layout, frames=frames)

# Displaying the figure
fig.show()
