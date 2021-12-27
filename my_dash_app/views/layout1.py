
from my_dash_app.maindash import app
from dash import dcc  # layout html
from dash import html, Input, Output, callback_context #funzioni di layout html interattivo
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate #funzioni di layout html interattivo
import plotly.graph_objects as go  # creazione grafici

from classeAnalisi import Analisi

italia = Analisi("Italy")

cina = Analisi("China")


"""
LAYOUT HTML
"""


def make_layout():
    return html.Div(id='parent', children=[
    html.Div(id='header', className='out-container', children=[
        html.Div(className='container', children=[
            html.H1(id='title', children='COVID-19 Dashboard'),
        ])
    ]),
    html.Div(className='container', children=[

        html.Div(id='covid', className='analisi', children=[
            html.H2(children='Analisi deceduti Italia'),
            html.Div(className='legenda', children=[
                html.P(children=('Media: ', round(italia.df.new_deaths.diff().mean(), 2))),
                html.P(children=('Massimo: ', italia.df.new_deaths.diff().max())),
                html.P(children=('Minimo: ', italia.df.new_deaths.diff().min())),
            ]),
            dcc.Graph(className='grafico', id='bar_plot', figure=italia.fig, responsive=True,
                      config={'responsive': True, 'autosizable': True}),
        ]),

        html.Div(id='ML', className='analisi', children=[
            html.H2(children='Analisi deceduti Cina'),
            html.Div(className='legenda', children=[
                html.P(children=('Media: ', round(cina.df.new_deaths.diff().mean(), 2))),
                html.P(children=('Massimo: ', cina.df.new_deaths.diff().max())),
                html.P(children=('Minimo: ', cina.df.new_deaths.diff().min())),
            ]),

            dcc.Graph(className='grafico', id='bar_plot1', figure=cina.fig, responsive=True),

        ]),
        html.Div(id='covidTot', className='analisi', children=[
            html.H2(children='Grafico Totale in Scala Logaritmica di tutte le colonne'),
            html.H3(children='Italia'),
            dcc.Graph(className='grafico', id='scatter_1', figure=italia.figTot, responsive=True,
                      config={'responsive': True, 'autosizable': True}),
            html.H3(children='Cina'),
            dcc.Graph(className='grafico', id='scatter_2', figure=cina.figTot, responsive=True,
                      config={'responsive': True, 'autosizable': True}),
        ]),
    ]),
    html.Div(id='image', className='out-container', children=[
        html.Img(src='https://i.ibb.co/8zkNZTT/7VE.gif')
        #
    ]),
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
