import pandas as pd
from datetime import date
from dash import dcc  
from dash import html  
import dash_bootstrap_components as dbc
import datetime
from appCovidData.assets.header import header
from appCovidData.assets.footer import footer


# function that creates a list of Nations 
def coutries_list():
    df = pd.read_csv("data/owid-dataset.csv")
    keep = ["location"]
    df = df[keep]
    return df['location'].unique()

# variables used by DateRangePicker as default values
oggi = date.today()
minDate = date(2020, 1, 1)
maxDate = oggi
monthVisible = oggi
startDate = oggi - datetime.timedelta(days=60)
endDate = oggi
startDateMondo = date(2020, 3, 1)
endDateMondo = date(2020, 5, 1)

# data list for Dropdown and Switch options 
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

# dictionaries to translate dataset columns' names (as an alias)
# dictionary for "confronto" (comparison) and "proiezione" (prediction) sections 
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
# dictionary for "World Data" section 
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

"""
LAYOUT HTML
"""

intro =dbc.Container([
    dbc.Row([
        dbc.Col([
            html.P(children="A metà dicembre 2019 le autorità sanitarie della città di Wuhan riscontrarono i "
                            "primi casi di pazienti che mostravano i sintomi di una polmonite grave, così ha avuto "
                            "inizio la pandemia che tutt’oggi stiamo ancora vivendo."),
            html.P(children="Il virus responsabile è stato "
                            "identificato e denominato nei primi giorni di gennaio 2020: Coronavirus 2 della Sindrome "
                            "Respiratoria Acuta Severa, abbreviato SARS-CoV-2. "),
            html.P(children="Lo scopo di covid-19 dashboard è quello "
                            "di racchiudere in un’unica pagina le informazioni provenienti da tutto il mondo per visionare "
                            "tramite grafici, i dati provenienti da più dataset, facilitando quindi, la lettura di "
                            "questi ultimi."),
        ],
        lg=8,
        width=12,
        className="mx-auto"),
    ])
],
className="mb-5")

menu = dbc.Container([
    dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.I(className="fas fa-globe-europe fa-4x mb-3"),
                    dbc.Button(html.H3(children=html.A(children="World data", href="#world-section", className="text-white text-decoration-none"), className="fs-5 text-white mb-0 py-2"),
                               color="primary",
                               className="w-100 mb-3"),
                    html.P(
                        children="Visualizza una mappa del mondo con un range di colori in base al dato scelto e alla "
                                 "variazione di quest’ultimo. ",
                        className="text-start")
                ],
                    width=12,
                    md=4,
                ),
                dbc.Col([
                    html.I(className="fas fa-balance-scale-left fa-4x mb-3"),
                    dbc.Button(html.H3(children=html.A(children="Fai un confronto", href="#compare-section", className="text-white text-decoration-none"), className="fs-5 text-white mb-0 py-2"),
                               color="primary",
                               className="w-100 mb-3"),
                    html.P(children="Ti permette di mettere a confronto dati diversi di stati diversi andando a "
                                    "scegliere i dati che si vogliono visualizzare.",
                           className="text-start")
                ],
                    width=12,
                    md=4,
                ),
                dbc.Col([
                    html.I(className="fas fa-chart-line fa-4x mb-3"),
                    dbc.Button(html.H3(children=html.A(children="Fai una proiezione", href="#ML-section", className="text-white text-decoration-none"), className="fs-5 text-white mb-0 py-2"),
                               color="primary",
                               className="w-100 mb-3"),
                    html.P(children="Ti permette di andare a prevedere l’andamento del dato selezionato in base "
                                    "all’utilizzo di due algoritmi per la previsione. ",
                           className="text-start")
                ],
                    width=12,
                    md=4,
                ),

            ],
                className="text-center"),
        ],
        width=12,
        lg=8,
        className="mx-auto")
    ]),
],
    fluid=False)],
    fluid=True,
    className="bg-dark py-5 my-5")


# World Data section 
mondo = dbc.Container([
    dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    html.H2(children="World data", className="fs-4 m-0"),
                ],
                width= 12,
                md = 3,
                className="bg-primary p-3"
                ),
                dbc.Col(
                width= 12,
                md = 9,
                className="bg-white text-dark p-3",
                # updating data and title of comparison section by callback 
                id="titolo-mondo"
                ),
            ],
            className="g-0",
            align="center"),
        ],
        className="p-0"),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col([
                        html.P(children="Scegli il dato da visualizzare:", className=""),
                        dbc.RadioItems(
                            # for loop to show options from data list  
                            options=[{'label': dictDatiMondo[i], 'value': i} for i in datiColMondo],
                            value="total_cases_per_million",
                            id="dato-input",
                            switch=True,
                            className="mb-3"
                        ),
                        html.P(children="Scegli il range di date:", className=""),
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=minDate,
                            max_date_allowed=maxDate,
                            initial_visible_month=monthVisible,
                            start_date=startDateMondo,
                            end_date=endDateMondo,
                            display_format='D/M/Y',
                            style={"font-size": "12px", }
                        ),
                    ],
                        lg=3,
                        width=12,
                        className="p-3"
                    ),
                    dbc.Col([
                        dcc.Loading(id="ls-loading-1", children=[
                            dcc.Graph(
                                # graph updated by callback 
                                id='fig-mondo',
                                responsive=True,
                                config={
                                    'responsive': True,
                                    'autosizable': True
                                },
                                style={
                                    "height": "500px",
                                    "min-height": "500px",
                                },
                                className="p-3"
                            )],
                                    type="default"),
                    ],
                        className="m-0 p-3 p-lg-0 bg-black",
                        lg=9,
                        width=12
                    )
                ],
                    className="w-100 m-0 p-0 g-0 border-white"),
            ],
            className="p-0"
        ),
        dbc.CardFooter("Data source: OWID - Our World In Data"),
    ],
    className="rounded"),
],
    className="p-0 mb-5",
    fluid=False,
    id="world-section"
)

# "confronto" (comparison) section 
analisiCovid = dbc.Container([
    dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    html.H2(children="Effettua un confronto", className="fs-4 m-0"),
                ],
                width= 12,
                md = 3,
                className="bg-primary p-3"
                ),
                dbc.Col(
                width= 12,
                md = 9,
                className="bg-white text-dark p-3",
                # updating data and title of comparison section by callback
                id="titolo-confronto"
                ),
            ],
            className="g-0",
            align="center"),
        ],
        className="p-0"),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col([
                        html.P(children="Scegli il range di date:", className=""),
                        dcc.DatePickerRange(
                            id='date-confronto',
                            min_date_allowed=minDate,
                            max_date_allowed=maxDate,
                            initial_visible_month=monthVisible,
                            start_date=startDate,
                            end_date=endDate,
                            display_format='D/M/Y',
                            style={"font-size": "12px", },
                            className="mb-3"
                        ),
                        html.P(children="Dato 1:",
                               className=""),
                        dcc.Dropdown(
                            # for loop to show options from data list
                            options=[{'label': dictDati[i], 'value': i} for i in datiCol],
                            value="total_cases",
                            id="dato-input-1",
                            className="text-black"
                        ),
                        dcc.Dropdown(
                            id='input-nazione-1',
                            #for loop to show options from Nation list
                            options=[{'label': i, 'value': i} for i in coutries_list()],
                            value='Italy',
                            className="mb-3 text-dark"
                        ),
                        html.P(children="Dato 2:", className=""),
                        dcc.Dropdown(
                            # for loop to show options from data list
                            options=[{'label': dictDati[i], 'value': i} for i in datiCol],
                            value="total_cases",
                            id="dato-input-2",
                            className="text-black"
                        ),
                        dcc.Dropdown(
                            id='input-nazione-2',
                            # for loop to show options from Nation list
                            options=[{'label': i, 'value': i} for i in coutries_list()],
                            value='Spain',
                            className="mb-3 text-dark"
                        ),
                    ],
                        lg=3,
                        width=12,
                        className="p-3"),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dcc.Loading(id="ls-loading-2", children=[
                                    dcc.Graph(
                                        # graph updated by callback 
                                        id='fig-confronto',
                                        responsive=True,
                                        config={
                                            'responsive': True,
                                            'autosizable': True
                                        },
                                        style={
                                            'height': '350px'
                                        },
                                    )],
                                            type="default")
                            ],
                                width=12,
                                align="bottom",
                                className="p-3"
                            ),
                        ]),
                        dbc.Row(
                            [
                                dbc.Col([],
                                    width=12,
                                    lg=6,
                                    className="p-3",
                                    # "dato1" table updated by callback  
                                    id="dati-nazione-1"
                                ),
                                dbc.Col([],
                                    width=12,
                                    lg=6,
                                    className="p-3",
                                    # "dato2" table updated by callback 
                                    id="dati-nazione-2"
                                ),
                            ],
                            className="mb-3 g-0"
                        ),
                    ],
                        className="m-0 p-3 p-lg-0 bg-black",
                        lg=9,
                        width=12
                    ),
                ],
                className="g-0"),
            ],
            className="p-0"
        ),
        dbc.CardFooter("Data source: OWID - Our World In Data"),
    ]),
],
    fluid=False,
    className="p-0",
    id="compare-section"
)


# "fai una proiezione" section (future prediction)
machineLearning = dbc.Container([
    dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    html.H2(children="Fai una proiezione", className="fs-4 m-0"),
                ],
                width= 12,
                md = 3,
                className="bg-primary p-3"
                ),
                dbc.Col(
                width= 12,
                md = 9,
                className="bg-white text-dark p-3",
                # updating prediction date and title  by callback 
                id="titolo-ML"
                ),
            ],
            className="g-0",
            align="center"),
        ],
        className="p-0"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P(children="Scegli il dato:", className=""),
                    dcc.Dropdown(
                        #for loop to show options from data list 
                        options=[{'label': dictDati[i], 'value': i} for i in datiCol],
                        value="total_cases",
                        id="dato-input-ML",
                        className="text-black mb-3"
                    ),
                    html.P(children="Scegli la nazione:", className=""),
                    dcc.Dropdown(
                        id='input-nazione-ML',
                        # for loop to show options from Nations list 
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
                            # prediction graph updated by callback 
                            id='fig-ML',
                            responsive=True,
                            config={
                                'responsive': True,
                                'autosizable': True
                            },
                            style={
                                'height': '350px'
                            },
                        ),
                    ]),
                ],
                    width=12,
                    lg=9,
                    align="bottom",
                    className="m-0 p-3 bg-black"
                ),
            ],
                className="g-0"),
        ],
                     className="p-0"),
        dbc.CardFooter(["Data source: OWID - Our World In Data"]),
    ]),
],
    fluid=False,
    className="p-0 rounded shadow bg-black my-5",
    id = "ML-section"
)

# defying function to create layout made of header, footer and the other sections 
def make_layout():
    return html.Div(id='parent', children=[
        header,
        intro,
        menu,
        mondo,
        analisiCovid,
        machineLearning,
        footer
    ])
