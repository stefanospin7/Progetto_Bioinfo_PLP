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

#NAVBAR

navbar = dbc.Container([
    html.H2(children="World COVID-19 dataset", className="fs-4 text-center text-white mb-4"),
    dbc.Navbar(
            dbc.Container([
                dbc.Row(
                    [
                        dbc.Col([
                            html.H3(children="1. Scegli il dato da visualizzare:", className="fs-5 bg-primary p-1"),
                            dbc.RadioItems(
                                #options=[{'label': i, 'value': i} for i in italia.df.columns],
                                options=[{'label': i, 'value': i} for i in datiCol],
                                #options=[{'label': 'Casi totali', 'value': 'total_cases'}, {'label': 'Nuove morti', 'value': 'new_deaths'}],
                                value="total_cases",
                                id="dato-input",
                                switch=True,
                                className="text-white"
                            ),
                            ],
                            width=12,
                            lg=6
                             ),
                        dbc.Col([
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

                        ],
                        width=12,
                        lg=6,
                        className=""),

                        # dbc.Col([
                        #     dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                        #     dbc.Collapse(
                        #         dbc.Nav(
                        #             [
                        #                 dcc.Link(dbc.NavItem(
                        #                         dbc.NavLink('Go to Page 1', active=True),
                        #                         ),
                        #                         href='/page-1',
                        #                          ),
                        #                 dcc.Link(dbc.NavItem(
                        #                         dbc.NavLink('Go to Page 2'),
                        #                         ),
                        #                         href='/page-2',
                        #                          )
                        #             ]
                        #         )
                        #         ,
                        #         id="navbar-collapse",
                        #         is_open=False,
                        #         navbar=True,
                        #         className="justify-content-end",
                        #     )
                        # ]),
                    ],
                    align="",
                    className="w-100 text-white",
                )],
                fluid=False,
            ),
        #color="white",
        dark=True,
        className="bg-transparent"
        )],
        fluid=True,
        className="p-0 py-5 bg-dark")


#ANALISI COVID
mondo = dbc.Container([
    dbc.Row([
        dbc.Col(
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
        width=12
        )
    ],
    className=""),
],
fluid=True,
className="m-0 p-0"
)

analisiCovid = dbc.Container([
    html.H2(children="Confronta 2 nazioni", className="fs-4 text-center mb-4"),
    dbc.Container([
        dbc.Row(
        [
        dbc.Col([
            html.H4(children="5. Scegli la nazione 1:", className="fs-5 mt-3 bg-primary p-1 bg-primary p-1 text-white"),
            dcc.Dropdown(
                id='input-nazione-1',
                options=[{'label': i, 'value': i} for i in coutries_list()],
                value='Italy',
                className="mb-3"
            ),
            html.H2(id="titolo-nazione-1"),
            html.Ul(
                className="list-group bg-light p-3",
                id ="dati-nazione-1")
            ],
            width=12,
            lg=4,
            #className="order-2 order-lg-1"
            ),
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
            lg=4,
            align="bottom",
            className="mt-5"
            ),
        dbc.Col([
            html.H4(children="6. Scegli la nazione 2:", className="fs-5 mt-3 bg-primary p-1 text-white"),
            dcc.Dropdown(
                id='input-nazione-2',
                options=[{'label': i, 'value': i} for i in coutries_list()],
                value='China',
                className="mb-3"
            ),
            html.H2(id="titolo-nazione-2"),
            html.Ul(
                className="list-group bg-light p-3",
                id ="dati-nazione-2")
            ],
            width=12,
            lg=4,
            #className="order-3 order-lg-3"
            ),
        ],
        #align="center",
        className="mb-3"
        ),
        ],
        fluid=False,
        className=""
        )
    ],
    fluid=True,
    className="bg-light mt-5 py-5"
    )



def make_layout():
    return html.Div(id='parent', children=[
        header,
        navbar,
        mondo,
        analisiCovid,
        footer
    ])