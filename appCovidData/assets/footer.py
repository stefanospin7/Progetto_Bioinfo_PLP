from dash import html  
import dash_bootstrap_components as dbc

# defying footer html layout 
footer = dbc.Container(
            dbc.Container([
                html.H4(children='Credits', className=''),
                dbc.Row([
                    dbc.Col([
                        html.P(children='Lavoro di gruppo', className='m-0'),
                        html.P(children='Corso di Programmazione e Laboratorio di Programmazione', className="fw-bold m-0"),
                        html.P(children='Bioinformatica - Tor Vergata'),
                        html.P(children=[html.Span(children='Docente: ', className="fw-bold"), html.Span(children='Daniele Pasquini')]),
                        html.A(
                            dbc.Row(
                                [
                                    dbc.Col([
                                        html.I(className="fab fa-github d-inline me-1"),
                                        html.P(children="Git-Hub app repository", className="d-inline"),
                                    ],
                                        width="auto",
                                        className=""),
                                ],
                                align="center",
                                className="g-0",
                            ),
                            href="https://github.com/stefanospin7/Progetto_Bioinfo_PLP",
                            style={"textDecoration": "none"},
                        )
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
            ]),
        fluid=True,
        className="text-light bg-dark py-5"
        )
