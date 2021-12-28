from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc
from appCovidData.classeAnalisi import Analisi

italia = Analisi("Italy")

cina = Analisi("China")


"""
LAYOUT HTML
"""


navbar = dbc.Navbar(
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            html.A(
                                # Use row and col to control vertical alignment of logo / brand
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.NavbarBrand(
                                            html.H1(children="COVID-19 Dashboard"),
                                            className="ms-2")),
                                    ],
                                    align="center",
                                    className="g-0",
                                ),
                                href="#",
                                style={"textDecoration": "none"},
                            )
                        ),
                        dbc.Col([
                            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dcc.Link(dbc.NavItem(
                                                dbc.NavLink('Go to Page 1', active=True),
                                                ),
                                                href='/page-1',
                                                 ),
                                        dcc.Link(dbc.NavItem(
                                                dbc.NavLink('Go to Page 2'),
                                                ),
                                                href='/page-2',
                                                 )
                                    ]
                                )
                                ,
                                id="navbar-collapse",
                                is_open=False,
                                navbar=True,
                                className="justify-content-end",
                            )
                        ]),
                    ],
                    align="center",
                    className="g-0 w-100",
                ),
                fluid=False,
            ),
    #color="white",
    dark=True,
    className="bg-transparent"
)

analisiCovid = dbc.Container([
    dbc.Row(
        html.H2(children='Italia'),
        className="mb-3 text-center"
        ),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in italia.df.columns],
                value='new_deaths',
                className="mb-3"
            ),
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
            className="list-group bg-light p-3"),
            ],
            width="3"
             ),
        dbc.Col(
            dcc.Graph(
                className='grafico',
                id='bar_plot',
                figure=italia.fig,
                responsive=True,
                config={
                    'responsive': True,
                    'autosizable': True
                },
                style={
                    'height': 300
                },
            )
            )
        ])
    ],
    className="mt-5"
    )

def make_layout():
    return html.Div(id='parent', children=[
        dbc.Container(navbar,
            fluid=True,
            className="p-0 bg-primary"),
        analisiCovid,
        html.Div(id='footer', className='out-container', children=[
            html.Div(className='container', children=[
                html.Div(className='credits', children=[
                    html.P(children='Lavoro di gruppo'),
                    html.P(children='Corso di Programmazione e Laboratorio di Programmazione'),
                    html.P(children='Bioinformatica - Tor Vergata'),
                    html.P(children='Docente: Daniele Pasquini'),
                ]),
                html.Ul(className='creditsR', children=[
                    html.P(children='Studenti:'),
                    html.Li(children='Manfredo Aristide Fraccola'),
                    html.Li(children='Sara Giordani'),
                    html.Li(children='Andrea Misiti'),
                    html.Li(children='Angela Sangiorgio'),
                    html.Li(children='Stefano Spinelli'),
                    html.Li(children='Gaia Tomei'),
                    html.Li(children='Alessandro Pucci'),
                ]),
            ])
        ]),
    ])