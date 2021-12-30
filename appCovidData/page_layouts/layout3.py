from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc

from appCovidData.classeAnalisi import Analisi

italia = Analisi("Italy")

cina = Analisi("China")


"""
LAYOUT HTML
"""

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

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
                                            dbc.NavLink('Go to Page 1', className="text-decoration-none"),
                                            className="text-decoration-none"
                                        ),
                                            href='/page-1',
                                            className="text-decoration-none"
                                        ),
                                        dcc.Link(dbc.NavItem(
                                            dbc.NavLink('Go to Page 2', active=True, style={"textDecoration": "none"}),
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
        html.H2(children='Cina'),
        className="mb-3 text-center"
        ),
    dbc.Row([
        dbc.Col([
            html.P(children=('Media: ', round(italia.df.new_deaths.diff().mean(), 2))),
            html.P(children=('Massimo: ', italia.df.new_deaths.diff().max())),
            html.P(children=('Minimo: ', italia.df.new_deaths.diff().min())),
            ],
            width="auto"
             ),
        dbc.Col(
            dcc.Graph(
                className='grafico',
                id='bar_plot',
                figure=cina.figTot,
                responsive=True,
                config={
                    'responsive': True,
                    'autosizable': True
                })
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
        analisiCovid
    ])