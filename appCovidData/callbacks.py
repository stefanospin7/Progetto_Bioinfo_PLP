import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from appCovidData.app import app
from dash import Input, Output, State  # funzioni di layout html interattivo
import time
import numpy as np

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("fig-mondo", "figure"),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def update_figMondo(input_dato, start_date, end_date):
    df = pd.read_csv("data/owid-dataset.csv",
                     parse_dates=["date"]
                     )
    df = df[df.location != 'World']
    periodo = (df['date'] > start_date) & (df['date'] <= end_date)
    df = df.loc[periodo]

    # Columns renaming
    df.columns = [col.lower() for col in df.columns]
    # Filling nan values with 0


    # Compute bubble sizes
    sizeInput = "size" + input_dato
    df[sizeInput] = df[input_dato].apply(
        lambda x: (np.sqrt(x / 1000) + 1) if x > 500 else (np.log(x) / 2 + 1)).replace(
        np.NINF, 0)

    # Compute bubble color
    colorInput = "color" + input_dato
    df[colorInput] = (df[input_dato] / df['total_cases']).fillna(0).replace(np.inf, 0)
    df = df.fillna(0).replace(np.inf, 0)

    days = df['date'].dt.date.unique().astype(str)

    df['date'] = df['date'].dt.date.astype(str)
    # days = ["2021-12-01", "2021-12-02"]
    #print(tmp.head(10))
    #colors = ["royalblue", "crimson", "lightseagreen", "orange", "lightgrey"]



    def generate_frame(day, input):
        sizeInput = "size"+input
        colorInput = "color"+input
        #print(sizeInput, colorInput, day, df[df["date"] == day])
        frame = {
            'name': 'frame_{}'.format(day),
            'data': {
                'type': 'scattermapbox',
                'lat': df[df["date"] == day]['latitude'],
                'lon': df[df["date"] == day]['longitude'],
                'marker': go.scattermapbox.Marker(
                    size=df[df["date"] == day][sizeInput],
                    color=df[df["date"] == day][colorInput],
                    #    showscale=True,
                    #    colorbar={'title':'Recovered', 'titleside':'top', 'thickness':4, 'ticksuffix':' %'},
                ),
                # 'customdata':np.stack((df.xs(day)['confirmed_display'], df.xs(day)['recovered_display'],  df.xs(day)['deaths_display'], pd.Series(df.xs(day).index)), axis=-1),
                # 'hovertemplate': "<extra></extra><em>%{customdata[3]}  </em><br>🚨  %{customdata[0]}<br>🏡  %{customdata[1]}<br>⚰️  %{customdata[2]}",
            }
        }
        return frame

    frames = []
    for day in days:
        frames.append(generate_frame(day, input_dato))

    #print(frames[0])

    sliders = [{
        'transition': {'duration': 0},
        'x': 0.08,
        'len': 0.88,
        'currentvalue': {'font': {'size': 15}, 'prefix': '📅 ', 'visible': True, 'xanchor': 'center'},
        'steps': [
            {
                'label': day,
                'method': 'animate',
                'args': [
                    ['frame_{}'.format(day)],
                    {'mode': 'immediate', 'frame': {'duration': 100, 'redraw': True}, 'transition': {'duration': 50}}
                ],
            } for day in days]
    }]

    # Defining the initial state
    data = frames[0]['data']

    # Adding all sliders and play button to the layout
    layout = go.Layout(
        sliders=sliders,
        # updatemenus=play_button,
        mapbox={
            'accesstoken': "pk.eyJ1IjoibWFuZnJlZG9mcmFjY29sYSIsImEiOiJja3hyd2JjbnEwNnVjMnBvNTZrbHBqdmwzIn0.YFYLdLUxoYC3gSpkcGplqQ",
            'center': {"lat": 37.86, "lon": 2.15},
            'zoom': 1.7,
            'style': 'light',
        }
    )

    # Creating the figure
    fig = go.Figure(data=data, layout=layout, frames=frames)


    time.sleep(1)
    return fig

