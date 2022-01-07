from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc

header = dbc.Container(dbc.Navbar(
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col([
                            html.A(
                                # Use row and col to control vertical alignment of logo / brand
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.NavbarBrand(
                                            html.Img(src="https://i.ibb.co/z56z80g/logo.png", style={"height": "80px"}),
                                            className="ms-2")),
                                    ],
                                    align="center",
                                    className="g-0",
                                ),
                                href="#",
                                style={"textDecoration": "none"},
                                className=""
                            )],
                            className="my-3",
                            width=12,
                            sm=6
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
                                            className="mx-auto mb-3"),
                                    ],
                                    align="center",
                                    className="g-0",
                                ),
                                href="https://github.com/stefanospin7/Progetto_Bioinfo_PLP",
                                style={"textDecoration": "none"},
                            ),
                            width=12,
                            sm=6,
                            className="text-center"
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