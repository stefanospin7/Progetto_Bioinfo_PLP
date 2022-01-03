from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc

header = dbc.Container(dbc.Navbar(
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            html.A(
                                # Use row and col to control vertical alignment of logo / brand
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.NavbarBrand(
                                            html.H1(children="COVID-19 Dashboard", className="fs-4"),
                                            className="ms-2")),
                                    ],
                                    align="center",
                                    className="g-0",
                                ),
                                href="#",
                                style={"textDecoration": "none"},
                            )
                        ),
                        dbc.Col(
                            html.A(
                                # Use row and col to control vertical alignment of logo / brand
                                dbc.Row(
                                    [
                                        dbc.Col([
                                            html.I(className="fab fa-github d-inline me-1"),
                                            html.P(children="Git-Hub app repository", className="d-inline"),
                                            ],
                                            width="auto",
                                            className="ms-auto"),
                                    ],
                                    align="center",
                                    className="g-0",
                                ),
                                href="https://github.com/stefanospin7/Progetto_Bioinfo_PLP",
                                style={"textDecoration": "none"},
                            )
                        ),
                    ],
                    align="center",
                    className="g-0 w-100",
                ),
                fluid=False,
            ),
        #color="white",
        dark=True,
        className="p-0 bg-transparent"
        ),
        fluid=True,
        className="p-0 bg-primary")