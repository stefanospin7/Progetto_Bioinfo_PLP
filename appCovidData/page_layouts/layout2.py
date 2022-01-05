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

italia = Analisi("Italy")
cina = Analisi("China")

def coutries_list():
    df = pd.read_csv("data/owid-dataset.csv")
    # df = df[df["location"] == "World"]
    keep = ["location"]
    df = df[keep]
    return df['location'].unique()

"""
LAYOUT HTML
"""

#oggi = date.today()


oggi = date.today() - datetime.timedelta(days=1)
ieri = oggi - datetime.timedelta(days=30)
futuro = oggi + datetime.timedelta(days=30)
futuroMax = oggi + datetime.timedelta(days=365)
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

#NAVBAR

navbar = dbc.Container([
    dbc.Navbar(
            dbc.Container([
                dbc.Collapse([
                    dbc.Row([
                        dbc.Col([
                    html.H3(children="1. Scegli il dato da visualizzare:", className="fs-5 bg-primary p-1"),
                    dbc.RadioItems(
                        # options=[{'label': i, 'value': i} for i in italia.df.columns],
                        options=[{'label': dictDati[i], 'value': i} for i in datiCol],
                        # options=[{'label': 'Casi totali', 'value': 'total_cases'}, {'label': 'Nuove morti', 'value': 'new_deaths'}],
                        value="total_cases",
                        id="dato-input",
                        switch=True,
                        className="text-white"
                    ),
                    html.H3(children="2. Scegli il range di date:", className="fs-5 bg-primary p-1"),
                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=date(2020, 3, 1),
                        max_date_allowed=oggi,
                        initial_visible_month=date(2021, 12, 1),
                        start_date=ieri,
                        end_date=oggi,
                        display_format='D/M/Y',
                    ),
                    html.H3(children="3. Seleziona per fare una previsione:", className="fs-5 mt-3 bg-primary p-1"),
                    dbc.Switch(
                        id="futuro-input",
                        label="Fai una previsione",
                        value=False,
                    ),
                    dcc.DatePickerSingle(
                        id='my-date-picker-single',
                        min_date_allowed=oggi,
                        max_date_allowed=futuroMax,
                        initial_visible_month=futuro,
                        date=futuro,
                    ),
                    html.H4(children="4. Scegli la nazione 1:", className="fs-5 mt-3 bg-primary p-1 bg-primary p-1 text-white"),
                    dcc.Dropdown(
                        id='input-nazione-1',
                        options=[{'label': i, 'value': i} for i in coutries_list()],
                        value='Italy',
                        className="mb-3"
                    ),
                    html.H4(children="5. Scegli la nazione 2:", className="fs-5 mt-3 bg-primary p-1 text-white"),
                    dcc.Dropdown(
                        id='input-nazione-2',
                        options=[{'label': i, 'value': i} for i in coutries_list()],
                        value='China',
                        className="mb-3"
                    ),
                        ],
                        className="p-3"),
                        ],
                        className="g-0"
                    ),
                    ],
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                    className="justify-content-center text-white",
                )
                ],
                fluid=True,
            ),
        #color="white",
        dark=True,
        className="bg-transparent p-0"
        )],
        fluid=True,
        className="container-fluid")


#ANALISI COVID
mondo = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Hr(style={'height': "4px", "width": "10%"}, className="mx-auto text-primary"),
            html.H2(children="World COVID-19 dataset", className="fs-4 text-center mb-4"),
            dcc.Loading(id="ls-loading-1", children=[
                dcc.Graph(
                    id='fig-mondo',
                    #figure=italia.figTot,
                    responsive=True,
                    config={
                        'responsive': True,
                        'autosizable': True
                    },
                    style={
                        "height": 500
                    },
                )],
            type="default"),
            ],
        width=12,
        className="m-0 p-0"
        )
    ],
    className="w-100 m-0 p-0"),
],
fluid=True,
className="m-0 p-0"
)

analisiCovid = dbc.Container([
    html.Hr(style={'height': "4px", "width": "10%"}, className="mx-auto text-primary"),
    html.H2(children="Confronta 2 nazioni", className="fs-4 text-center mb-4"),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Loading(id="ls-loading-2", children=[
                    dcc.Graph(
                        id='fig-confronto',
                        #figure=italia.figTot,
                        responsive=True,
                        config={
                            'responsive': True,
                            'autosizable': True
                        },
                        style={
                            'height': '330px'
                        },
                    )],
                type="default")
                ],
                width=12,
                lg=12,
                align="bottom",
                className=""
                ),
            ],
        className="g-0"),
        dbc.Row(
        [
        dbc.Col([
            html.H2(id="titolo-nazione-1"),
            html.Ul(
                className="list-group bg-light",
                id ="dati-nazione-1")
            ],
            width=12,
            lg=6,
            className="p-3"
            ),
        dbc.Col([
            html.H2(id="titolo-nazione-2"),
            html.Ul(
                className="list-group bg-light",
                id ="dati-nazione-2")
            ],
            width=12,
            lg=6,
            className="p-3"
            ),
        ],
        #align="center",
        className="mb-3 g-0"
        ),
        ],
        fluid=True,
        className=""
        )
    ],
    fluid=True,
    className="bg-light mt-5 py-5"
    )



def make_layout():
    return html.Div(id='parent', children=[
        header,
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0, className="p-0"),
                    navbar],
                        width="auto",
                        className="bg-dark shadow top-10 text-white",
                        style={"zIndex": 2000}),
                dbc.Col([
                        html.H2(id="titolo-dato", className="text-center bg-white py-3 shadow"),
                        mondo,
                        analisiCovid
                ])
            ],
            className="g-0")
        ],
        fluid=True,
        className="m-0 p-0"),
        footer
    ])