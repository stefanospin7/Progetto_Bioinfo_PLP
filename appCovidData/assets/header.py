from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc

#NAVBAR
navbar = dbc.Container(dbc.Navbar(
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
        ),
        fluid=True,
        className="p-0 bg-primary")

