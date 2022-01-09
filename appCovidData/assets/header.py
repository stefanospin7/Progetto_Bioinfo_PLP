from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc

header = dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(src="https://i.ibb.co/BfCMHLZ/logo-Tavola-disegno-1.png", style={"height": "80px"}),
                        className="text-center"
                    ),
                ],
                align="center",
                className="g-0",
            ),
        fluid=True,
        className="mt-3 p-4 mb-4")