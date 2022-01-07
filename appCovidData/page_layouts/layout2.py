import pandas as pd
from datetime import date
from dash import dcc  # layout html
from dash import html  # funzioni di layout html interattivo
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

# oggi = date.today()


oggi = date.today() - datetime.timedelta(days=1)
ieri = oggi - datetime.timedelta(days=30)
futuro = oggi + datetime.timedelta(days=30)
futuroMax = oggi + datetime.timedelta(days=365)
datiCol = ["icu_patients", "icu_patients_per_million", "new_cases", "new_cases_per_million", "new_deaths",
           "new_deaths_per_million", "new_tests", "new_tests_per_thousand", "new_vaccinations",
           "people_fully_vaccinated", "people_fully_vaccinated_per_hundred", "people_vaccinated",
           "people_vaccinated_per_hundred", "positive_rate", "total_boosters", "total_boosters_per_hundred",
           "total_cases", "total_cases_per_million", "total_deaths", "total_deaths_per_million", "total_tests",
           "total_tests_per_thousand", "total_vaccinations", "total_vaccinations_per_hundred"]
datiColMondo = ["icu_patients_per_million", "new_cases_per_million", "new_deaths_per_million", "new_tests_per_thousand",
                "people_fully_vaccinated_per_hundred", "people_vaccinated_per_hundred", "total_boosters_per_hundred",
                "total_cases_per_million", "total_deaths_per_million", "total_tests_per_thousand",
                "total_vaccinations_per_hundred"]
dictDati = {
    "icu_patients": "Terapia Intensiva",
    "icu_patients_per_million": "Terapia Intensiva per milione",
    "new_cases": "Casi giornalieri",
    "new_cases_per_million": "Casi giornalieri per milione",
    "new_deaths": "Decessi giornalieri",
    "new_deaths_per_million": "Decessi giornalieri per milione",
    "new_tests": "Tamponi giornalieri",
    "new_tests_per_thousand": "Tamponi per centinaia",
    "new_vaccinations": "Vaccinazioni giornaliere",
    "people_fully_vaccinated": "Vaccinati completamente",
    "people_fully_vaccinated_per_hundred": "Vaccinati completamente per centinaia",
    "people_vaccinated": "Vaccinati totali",
    "people_vaccinated_per_hundred": "Vaccinati totali per centinaia",
    "positive_rate": "Tasso di positività",
    "total_boosters": "Dosi booster totali",
    "total_boosters_per_hundred": "Dosi booster totali per centinaia",
    "total_cases": "Casi totali",
    "total_cases_per_million": "Casi totali per milione",
    "total_deaths": "Decessi totali",
    "total_deaths_per_million": "Decessi totali per milione",
    "total_tests": "Tamponi totali",
    "total_tests_per_thousand": "Tamponi totali per migliaia",
    "total_vaccinations": "Dosi somministrate totali",
    "total_vaccinations_per_hundred": "Dosi somministrate per centiania",
}

dictDatiMondo = {
    "icu_patients_per_million": "Terapia Intensiva",
    "new_cases_per_million": "Casi giornalieri",
    "new_deaths_per_million": "Decessi giornalieri",
    "new_tests_per_thousand": "Tamponi",
    "people_fully_vaccinated_per_hundred": "Vaccinati completamente",
    "people_vaccinated_per_hundred": "Vaccinati totali",
    "total_boosters_per_hundred": "Dosi booster totali",
    "total_cases_per_million": "Casi totali",
    "total_deaths_per_million": "Decessi totali",
    "total_tests_per_thousand": "Tamponi totali",
    "total_vaccinations_per_hundred": "Dosi somministrate",
}

# FIGURA MONDO
mondo = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Hr(style={'height': "4px", "width": "10%"}, className="mx-auto text-white"),
            html.H2(children="World COVID-19 dataset", className="fs-4 text-center mb-4 fw-lighter"),
            html.H3(id="titolo-dato", className="bg-success text-center py-3 shadow"),
            html.P(children="Scegli il dato da visualizzare:", className="bg-primary p-2"),
            dbc.RadioItems(
                # options=[{'label': i, 'value': i} for i in italia.df.columns],
                options=[{'label': dictDatiMondo[i], 'value': i} for i in datiColMondo],
                # options=[{'label': 'Casi totali', 'value': 'total_cases'}, {'label': 'Nuove morti', 'value': 'new_deaths'}],
                value="total_cases_per_million",
                id="dato-input",
                switch=True,
                className="mb-3"
            ),
            html.P(children="Scegli il range di date:", className="bg-primary p-2"),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(2020, 3, 1),
                max_date_allowed=oggi,
                initial_visible_month=date(2021, 12, 1),
                start_date=date(2020, 3, 1),
                end_date=date(2020, 10, 1),
                display_format='D/M/Y',
            ),
        ],
            lg=3,
            width=12,
            className="p-3 pb-3"
        ),
        dbc.Col([
            dcc.Loading(id="ls-loading-1", children=[
                dcc.Graph(
                    id='fig-mondo',
                    # figure=italia.figTot,
                    responsive=True,
                    config={
                        'responsive': True,
                        'autosizable': True
                    },
                    style={
                        "height": "80vh"
                    },
                    className="pb-3"
                )],
                        type="default"),
        ],
            className="m-0 p-3 p-lg-0",
            lg=9,
            width=12
        )
    ],
        className="w-100 m-0 p-0"),
],
    fluid=False,
    className="p-0 rounded shadow bg-black mt-5 container"
)

analisiCovid = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Hr(style={'height': "4px", "width": "10%"}, className="mx-auto text-white"),
                    html.H2(children="Confronta 2 nazioni", className="fs-4 text-center mb-4 fw-lighter"),
                    html.P(children="Scegli la nazione 1:",
                           className="bg-primary p-2"),
                    dcc.Dropdown(
                        id='input-nazione-1',
                        options=[{'label': i, 'value': i} for i in coutries_list()],
                        value='Italy',
                        className="mb-3 text-dark"
                    ),
                    html.P(children="Scegli la nazione 2:", className="bg-primary p-2"),
                    dcc.Dropdown(
                        id='input-nazione-2',
                        options=[{'label': i, 'value': i} for i in coutries_list()],
                        value='China',
                        className="mb-3 text-dark"
                    ),
                ],
                    className="p-3"),
            ],
                className="w-100 m-0 p-0"
            ),
        ],
            lg=3,
            width=12,
            className="p-3 pb-3"),
        dbc.Col([
            dbc.Row(
                [
                    dbc.Col([
                        html.H2(id="titolo-nazione-1", className="bg-success text-center py-3 shadow"),
                        html.Ul(
                            className="list-group bg-light",
                            id="dati-nazione-1")
                    ],
                        width=12,
                        lg=6,
                        className="p-3"
                    ),
                    dbc.Col([
                        html.H2(id="titolo-nazione-2", className="bg-success text-center py-3 shadow"),
                        html.Ul(
                            className="list-group bg-light",
                            id="dati-nazione-2")
                    ],
                        width=12,
                        lg=6,
                        className="p-3"
                    ),
                ],
                # align="center",
                className="mb-3 g-0"
            ),
        ],
            className="m-0 p-3 p-lg-0",
            lg=9,
            width=12
        ),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Loading(id="ls-loading-2", children=[
                dcc.Graph(
                    id='fig-confronto',
                    # figure=italia.figTot,
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
            align="bottom",
            className="p-3"
        ),
    ])
],
    fluid=False,
    className="p-0 rounded shadow bg-black mt-5 container"
)

machineLearning = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Hr(style={'height': "4px", "width": "10%"}, className="mx-auto text-white"),
            html.H2(children="Fai una proiezione", className="fs-4 text-center mb-4 fw-lighter"),
            html.P(children="Scegli il dato:", className="bg-primary p-2"),
            dcc.Dropdown(
                # options=[{'label': i, 'value': i} for i in italia.df.columns],
                options=[{'label': dictDati[i], 'value': i} for i in datiCol],
                # options=[{'label': 'Casi totali', 'value': 'total_cases'}, {'label': 'Nuove morti', 'value': 'new_deaths'}],
                value="total_cases",
                id="dato-input-ML",
                # switch=True,
                className="text-black"
            ),
            html.P(children="Scegli la nazione:", className="bg-primary p-2"),
            dcc.Dropdown(
                id='input-nazione-ML',
                options=[{'label': i, 'value': i} for i in coutries_list()],
                value='Italy',
                className="mb-3 text-black"
            ),
        ],
            lg=3,
            width=12,
            className="p-3"
        ),
        dbc.Col([
            dcc.Loading(id="ls-loading-3", children=[
                dcc.Graph(
                    id='fig-ML',
                    # figure= fig,
                    responsive=True,
                    config={
                        'responsive': True,
                        'autosizable': True
                    },
                    style={
                        #  'height': '330px'
                    },
                ),
            ]),
        ],
            width=12,
            lg=9,
            align="bottom",
            className="p-3"
        ),
    ],
        className="g-0"),
],
    fluid=False,
    className="p-0 rounded shadow bg-black my-5"
)


def make_layout():
    return html.Div(id='parent', children=[
        header,
        mondo,
        analisiCovid,
        machineLearning,
        footer
    ])
