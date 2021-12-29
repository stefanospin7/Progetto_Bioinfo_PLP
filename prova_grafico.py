import pandas as pd
import numpy as np
import plotly.graph_objects as go


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
    df['size'] = df['total_cases'].apply(lambda x: (np.sqrt(x / 100) + 1) if x > 500 else (np.log(x) / 2 + 1)).replace(
        np.NINF, 0)

    # Compute bubble color
    df['color'] = (df['new_cases'] / df['total_cases']).fillna(0).replace(np.inf, 0)

    return df

df = process_pandemic_data(df)
print(df.head(5))

df_iso = pd.read_csv('https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv')
print(df_iso.head(5))


# Selecting the day to display
day = '2020-03-08'
tmp = df[df["date"] == day]
#tmp = df.xs(day)

# Create the figure and feed it all the prepared columns
fig = go.Figure(
    go.Scattermapbox(
        locations=tmp['iso_code'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=tmp['size'],
            color=tmp['color']
        )
    )
)

# Specify layout information
fig.update_layout(
    mapbox=dict(
        accesstoken='pk.eyJ1IjoibWFuZnJlZG9mcmFjY29sYSIsImEiOiJja3hyd2JjbnEwNnVjMnBvNTZrbHBqdmwzIn0.YFYLdLUxoYC3gSpkcGplqQ',
        center=go.layout.mapbox.Center(lat=45, lon=-73),
        zoom=1
    )
)

# Display the figure
fig.show()