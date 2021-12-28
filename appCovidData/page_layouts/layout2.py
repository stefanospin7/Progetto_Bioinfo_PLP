import pandas as pd
from datetime import date
from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc
from appCovidData.classeAnalisi import Analisi
from appCovidData.assets.header import navbar
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

oggi = date.today()

#ANALISI COVID
analisiCovid = dbc.Container([
    dbc.Row(
        [
            dbc.Col([
                html.H2(children='Italia'),
                ],
                width="auto"
            ),
            dbc.Col([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in coutries_list()],
                    value='italy',
                    className="mb-3"
                ),
            ],
            width=3),
            dbc.Col([
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=date(2020, 3, 1),
                    max_date_allowed=oggi,
                    initial_visible_month=date(2020, 3, 1),
                    end_date=oggi
                ),
            ],
            width=3,
            className="ms-auto")
        ],
        align="center",
        className="mb-3"
        ),
    dbc.Row([
        dbc.Col([
            dbc.Checklist(
                options=[{'label': i, 'value': i} for i in italia.df.columns],
                value=["new_cases"],
                id="dato-input",
                switch=True,
            )
            ],
            width="3"
             ),
        dbc.Col(
            dcc.Graph(
                className='grafico',
                id='bar_plot',
                figure=italia.figTot,
                responsive=True,
                config={
                    'responsive': True,
                    'autosizable': True
                },
                style={
                    'height': 300
                },
            )
            ),
        dbc.Col([
            html.Ul(children=([
                html.Li(children=([
                    dbc.Row([
                        dbc.Col([
                            html.I(className="fas fa-virus me-3"),
                            html.Span(
                                children=("Media")
                            )
                        ],
                        width=7,
                        className="p-3 bg-primary text-white"),
                        dbc.Col([
                            html.Span(
                                children=(round(italia.df.new_deaths.diff().mean(), 2)),
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
                                children=("Minimo")
                            )
                        ],
                        width=7,
                        className="p-3 bg-primary text-white"),
                        dbc.Col([
                            html.Span(
                                children=(italia.df.new_deaths.diff().min()),
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
                                children=(italia.df.new_deaths.diff().max()),
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
            ]),
            className="list-group bg-light p-3")
        ])
    ])
],
className="mt-5"
)



def make_layout():
    return html.Div(id='parent', children=[
        navbar,
        analisiCovid,
        footer
    ])