from dash import dcc  # layout html
from dash import html  #funzioni di layout html interattivo
import dash_bootstrap_components as dbc

#FOOTER

footer = dbc.Container(
            dbc.Container(
                dbc.Row([
                    dbc.Col([
                        html.P(children='Lavoro di gruppo', className='m-0'),
                        html.P(children='Corso di Programmazione e Laboratorio di Programmazione', className="fw-bold m-0"),
                        html.P(children='Bioinformatica - Tor Vergata'),
                        html.P(children=[html.Span(children='Docente: ', className="fw-bold"), html.Span(children='Daniele Pasquini')]),
                        ]
                    ),
                    dbc.Col([
                        html.P(children='Studenti:', className="fw-bold"),
                        html.Ul(className='list-unstyled', children=[
                            html.Li(children=[html.P(children='Manfredo Aristide Fraccola', className='m-0'),]),
                            html.Li(children=[html.P(children='Sara Giordani', className='m-0')]),
                            html.Li(children=[html.P(children='Andrea Misiti', className='m-0')]),
                            html.Li(children=[html.P(children='Alessandro Pucci', className='m-0')]),
                            html.Li(children=[html.P(children='Angela Sangiorgio', className='m-0')]),
                            html.Li(children=[html.P(children='Stefano Spinelli', className='m-0')]),
                            html.Li(children=[html.P(children='Gaia Tomei', className='m-0')]),
                        ])
                    ])
                ]),
            ),
        fluid=True,
        className="text-dark bg-light py-5"
        )