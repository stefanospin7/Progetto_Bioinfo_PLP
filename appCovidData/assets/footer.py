from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc

#FOOTER

footer = dbc.Container(
            dbc.Container(
                dbc.Row([
                    dbc.Col([
                        html.P(children='Lavoro di gruppo'),
                        html.P(children='Corso di Programmazione e Laboratorio di Programmazione'),
                        html.P(children='Bioinformatica - Tor Vergata'),
                        html.P(children='Docente: Daniele Pasquini'),
                        ]
                    ),
                    dbc.Col([
                        html.P(children='Studenti:'),
                        html.Ul(className='creditsR', children=[
                            html.Li(children='Manfredo Aristide Fraccola'),
                            html.Li(children='Sara Giordani'),
                            html.Li(children='Andrea Misiti'),
                            html.Li(children='Angela Sangiorgio'),
                            html.Li(children='Stefano Spinelli'),
                            html.Li(children='Gaia Tomei'),
                            html.Li(children='Alessandro Pucci')
                        ])
                    ])
                ]),
            ),
        fluid=True,
        className="text-white bg-dark pt-3"
        )