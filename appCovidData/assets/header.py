from dash import html  
import dash_bootstrap_components as dbc

# defying header html layout 
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
