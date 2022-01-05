import pandas as pd
from datetime import date
from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc
from appCovidData.classeAnalisi import Analisi
import datetime
from datetime import date
from appCovidData.assets.header import header
from appCovidData.assets.footer import footer
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta, date

datiCol = ["total_cases", "new_cases", "new_deaths", "new_vaccinations", "people_vaccinated", "people_fully_vaccinated", "total_boosters"]

dictDati =	{
    "total_cases": "Casi totali",
    "new_cases": "Casi giornalieri",
    "new_deaths": "Decessi giornalieri",
    "new_vaccinations": "Vaccinazioni giornaliere",
    "people_vaccinated": "Vaccinati totali",
    "people_fully_vaccinated": "Vaccinati con terza dose totali",
    "total_boosters": "Terze dosi totali",
}

def coutries_list():
    df = pd.read_csv("data/owid-dataset.csv")
    # df = df[df["location"] == "World"]
    keep = ["location"]
    df = df[keep]
    return df['location'].unique()




"""
LAYOUT HTML
"""

machineLearning = dbc.Container([
    html.H2(children="Test Machine Learning", className=""),
    html.H3(children="1. Scegli il dato da visualizzare:", className="fs-5 bg-primary p-1"),
    dbc.RadioItems(
        # options=[{'label': i, 'value': i} for i in italia.df.columns],
        options=[{'label': dictDati[i], 'value': i} for i in datiCol],
        # options=[{'label': 'Casi totali', 'value': 'total_cases'}, {'label': 'Nuove morti', 'value': 'new_deaths'}],
        value="total_cases",
        id="dato-input-ML",
        switch=True,
        className=""
    ),
    html.H4(children="Scegli la nazione:", className=""),
    dcc.Dropdown(
        id='input-nazione-ML',
        options=[{'label': i, 'value': i} for i in coutries_list()],
        value='Italy',
        className="mb-3"
    ),
    dcc.Graph(
                        id='fig-ML',
                        #figure= fig,
                        responsive=True,
                        config={
                            'responsive': True,
                            'autosizable': True
                        },
                        style={
                          #  'height': '330px'
                        },
                    )

                    ],
                    className="",
                    id="",
                    fluid=True
                                )

def make_layout():
    return html.Div(id='parent', children=[
        header,
        machineLearning,
        footer
    ])