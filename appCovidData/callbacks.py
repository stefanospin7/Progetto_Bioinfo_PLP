import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from appCovidData.app import app
from dash import Input, Output, State  # funzioni di layout html interattivo
import time
import numpy as np
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc
from appCovidData.classeAnalisi import Analisi

datiCol = ["total_cases", "new_cases", "new_deaths", "new_vaccinations", "people_vaccinated", "people_fully_vaccinated", "total_boosters"]

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
    Input('my-date-picker-range', 'end_date'),
    Input('futuro-input', 'value'),
    Input('my-date-picker-single', 'date'),
)
def update_figMondo(input_dato, start_date, end_date, futuro_input, future_date):
    df = pd.read_csv("data/owid-dataset.csv",
                     parse_dates=["date"]
                     )
    # Filter and clean df
    locationDel = ['World','Asia', 'Africa', 'Oceania', 'Europe', 'High income', 'Upper middle income', 'Lower middle income', 'North America', 'South America', 'European Union']
    df = df[~df.location.isin(locationDel)]
    print(df.location.unique())

    #df = df[df.location != 'World']

    if (futuro_input == False):
        periodo = (df['date'] > start_date) & (df['date'] <= end_date)
    else:
        periodo = (df['date'] > start_date) & (df['date'] <= future_date)
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

        customDataList = []
        for i in datiCol:
            customDataList.append(df[df["date"] == day][i])


        hoverTemplateList = []
        for i in datiCol:
            hoverTemplateList.append("%{customdata["+i+"]}  <br>")


        frame = {
            'name': 'frame_{}'.format(day),
            'data': {
                'type': 'scattermapbox',
                'lat': df[df["date"] == day]['latitude'],
                'lon': df[df["date"] == day]['longitude'],
                'marker': go.scattermapbox.Marker(
                    size=df[df["date"] == day][sizeInput],
                    #color=df[df["date"] == day][colorInput],
                    #color=df[df["date"] == day][colorInput],
                    #    showscale=True,
                    #    colorbar={'title':'Recovered', 'titleside':'top', 'thickness':4, 'ticksuffix':' %'},
                ),
                'customdata':np.stack((df[df["date"] == day]['location'], df[df["date"] == day]['total_cases'],  df[df["date"] == day]['new_cases'], df[df["date"] == day]['new_deaths']), axis=-1),
                'hovertemplate': "<extra></extra><em>%{customdata[0]}  </em><br>Total cases  %{customdata[1]}<br>New Cases  %{customdata[2]}<br>New deaths️  %{customdata[3]}",
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
        'currentvalue': {'font': {'size': 15}, 'prefix': 'Date: ', 'visible': True, 'xanchor': 'center'},
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

    play_button = [{
        'type': 'buttons',
        'showactive': True,
        'x': 0.045, 'y': -0.08,
        'buttons': [{
            'label': '🎬',  # Play
            'method': 'animate',
            'args': [
                None,
                {
                    'frame': {'duration': 100, 'redraw': True},
                    'transition': {'duration': 50},
                    'fromcurrent': True,
                    'mode': 'immediate',
                }
            ]
        }]
    }]

    # Adding all sliders and play button to the layout
    layout = go.Layout(
        sliders=sliders,
        updatemenus=[{
        'type': 'buttons',
        'showactive': True,
        'x': 0.045, 'y': -0.08,
        'buttons': [{
            'label': '🎬',  # Play
            'method': 'animate',
            'args': [
                None,
                {
                    'frame': {'duration': 100, 'redraw': True},
                    'transition': {'duration': 50},
                    'fromcurrent': True,
                    'mode': 'immediate',
                }
            ]
        }]
    }],
        mapbox={
            'accesstoken': "pk.eyJ1IjoibWFuZnJlZG9mcmFjY29sYSIsImEiOiJja3hyd2JjbnEwNnVjMnBvNTZrbHBqdmwzIn0.YFYLdLUxoYC3gSpkcGplqQ",
            'center': {"lat": 37.86, "lon": 2.15},
            'zoom': 1.7,
            'style': 'light',
        },
        legend = dict(
            yanchor="top",
            y=0.97,
            xanchor="left",
            x=0.01),
        margin = {'l': 0, 'r': 0, 't': 0, 'b': 0},
        #showlegend = True
    )


    # Creating the figure
    fig = go.Figure(data=data, layout=layout, frames=frames)


    time.sleep(1)
    return fig

# update country 1 on input
@app.callback(
    Output("dati-nazione-1", "children"),
    Input('input-nazione-1', 'value'),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
)
def updateNazione(nazione, datoInput, start_date, end_date):
    df = Analisi(nazione).df
    #df['date'] = pd.to_datetime(df['date'])
    df = df[df.location == nazione]
    periodo = (df.index > start_date) & (df.index <= end_date)
    datiCol = [datoInput]
    # mldt.append(i)
    df = df[datiCol]
    df = df.loc[periodo]

    outputNazione = ([
        html.Li(children=([
            dbc.Row([
                dbc.Col([
                    html.I(className="fas fa-virus me-3"),
                    html.Span(
                        children=("Media"),
                    )
                ],
                    width=7,
                    className="p-3 bg-primary text-white"),
                dbc.Col([
                    html.Span(
                        children=(round(df[datoInput].mean(), 2)),
                        className="mr-3",
                        id="media-1"
                    )
                ],
                    width=5,
                    className="justify-content-center align-items-center d-flex",
                )
            ],
                className="w-100 m-0"),
        ]),
            className="list-group-item p-0 mb-3"),
        html.Li(children=([
            dbc.Row([
                dbc.Col([
                    html.I(className="fas fa-virus me-3"),
                    html.Span(
                        children=("Minimo")
                    )
                ],
                    width=7,
                    className="p-3 bg-primary text-white"),
                dbc.Col([
                    html.Span(
                        children=(df[datoInput].min()),
                        className="mr-3"
                    )
                ],
                    width=5,
                    className="justify-content-center align-items-center d-flex",
                )
            ],
                className="w-100 row m-0"),
        ]),
            className="list-group-item p-0 mb-3"),
        html.Li(children=([
            dbc.Row([
                dbc.Col([
                    html.I(className="fas fa-virus me-3"),
                    html.Span(
                        children=("Massimo")
                    )
                ],
                    width=7,
                    className="p-3 bg-primary text-white"),
                dbc.Col([
                    html.Span(
                        children=(df[datoInput].max()),
                        className="mr-3"
                    )
                ],
                    width=5,
                    className="justify-content-center align-items-center d-flex",
                )
            ],
                className="w-100 row m-0"),
        ]),
            className="list-group-item p-0"),
    ])
    return outputNazione

# update country1 Title
@app.callback(
    Output("titolo-nazione-1", "children"),
    Input('input-nazione-1', 'value'),
)
def updateNazioneTit(nazione):
    return nazione

# update country 2 on input
@app.callback(
    Output("dati-nazione-2", "children"),
    Input('input-nazione-2', 'value'),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
)
def updateNazione(nazione, datoInput, start_date, end_date):
    df = Analisi(nazione).df
    #df['date'] = pd.to_datetime(df['date'])
    df = df[df.location == nazione]
    periodo = (df.index > start_date) & (df.index <= end_date)
    datiCol = [datoInput]
    # mldt.append(i)
    df = df[datiCol]
    df = df.loc[periodo]

    outputNazione = ([
        html.Li(children=([
            dbc.Row([
                dbc.Col([
                    html.I(className="fas fa-virus me-3"),
                    html.Span(
                        children=("Media"),
                    )
                ],
                    width=7,
                    className="p-3 bg-primary text-white"),
                dbc.Col([
                    html.Span(
                        children=(round(df[datoInput].mean(), 2)),
                        className="mr-3",
                        id="media-1"
                    )
                ],
                    width=5,
                    className="justify-content-center align-items-center d-flex",
                )
            ],
                className="w-100 m-0"),
        ]),
            className="list-group-item p-0 mb-3"),
        html.Li(children=([
            dbc.Row([
                dbc.Col([
                    html.I(className="fas fa-virus me-3"),
                    html.Span(
                        children=("Minimo")
                    )
                ],
                    width=7,
                    className="p-3 bg-primary text-white"),
                dbc.Col([
                    html.Span(
                        children=(df[datoInput].min()),
                        className="mr-3"
                    )
                ],
                    width=5,
                    className="justify-content-center align-items-center d-flex",
                )
            ],
                className="w-100 row m-0"),
        ]),
            className="list-group-item p-0 mb-3"),
        html.Li(children=([
            dbc.Row([
                dbc.Col([
                    html.I(className="fas fa-virus me-3"),
                    html.Span(
                        children=("Massimo")
                    )
                ],
                    width=7,
                    className="p-3 bg-primary text-white"),
                dbc.Col([
                    html.Span(
                        children=(df[datoInput].max()),
                        className="mr-3"
                    )
                ],
                    width=5,
                    className="justify-content-center align-items-center d-flex",
                )
            ],
                className="w-100 row m-0"),
        ]),
            className="list-group-item p-0"),
    ])
    return outputNazione

# update country1 Title
@app.callback(
    Output("titolo-nazione-2", "children"),
    Input('input-nazione-2', 'value'),
)
def updateNazioneTit(nazione):
    return nazione

# update fig compare 2 countries
@app.callback(
    Output("fig-confronto", "figure"),
    Input('input-nazione-1', 'value'),
    Input('input-nazione-2', 'value'),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    )
def updateFigConfronto(nazione1, nazione2, datoInput, start_date, end_date ):

    def generateDf(nazione):
        df = Analisi(nazione).df
        # df['date'] = pd.to_datetime(df['date'])
        df = df[df.location == nazione]
        periodo = (df.index > start_date) & (df.index <= end_date)
        datiCol = [datoInput]
        # mldt.append(i)
        df = df[datiCol]
        df = df.loc[periodo]
        return df

    df1 = generateDf(nazione1)
    df2 = generateDf(nazione2)

    # Creating the figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1.index, y=df1[datoInput], name=nazione1, fill='tonexty', connectgaps=True))
    fig.add_trace(go.Scatter(x=df2.index, y=df2[datoInput], name=nazione2, fill='tonexty', connectgaps=True))
    fig.update_yaxes(type="log")
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.97,
            xanchor="left",
            x=0.01),
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        showlegend=True
    )
    fig.update_xaxes(range=[start_date, end_date])

    time.sleep(1)
    return fig