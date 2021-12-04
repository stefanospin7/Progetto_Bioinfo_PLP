
from my_dash_app.maindash import app
from dash import dcc  # layout html
from dash import html, Input, Output, callback_context #funzioni di layout html interattivo
from dash.exceptions import PreventUpdate #funzioni di layout html interattivo
import plotly.graph_objects as go  # creazione grafici

from analisi1 import dfVaxDeceduti, dfVax, fig3, fig2, fig1
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
        html.Div(className='analisi', children=[
            html.H2(children='Vaccinazioni: dosi somministrate'),
            html.Div(id='menutest', children=[
                html.Button('Prima Dose', id='btn-1', value='seconda_dose'),
                html.Button('Seconda Dose', id='btn-2', value='pregressa_infezione'),
                html.Button('Terza Dose', id='btn-3', value='dose_addizionale_booster')]),
            dcc.Graph(id='graph-with-slider', figure=fig3),
        ]),

        html.Div(id='covid', className='analisi', children=[
            html.H2(children='Analisi decessi / vaccinazioni'),
            html.Div(className='legenda', children=[
                html.P(children=('Media: ', round(dfVaxDeceduti.deceduti.diff().mean(), 2))),
                html.P(children=('Massimo: ', dfVaxDeceduti.deceduti.diff().max())),
                html.P(children=('Minimo: ', dfVaxDeceduti.deceduti.diff().min())),
            ]),
            dcc.Graph(className='grafico', id='bar_plot', figure=fig1, responsive=True,
                      config={'responsive': True, 'autosizable': True}),
        ]),

        html.Div(id='ML', className='analisi', children=[
            html.H2(children='Analisi decessi con machine learning Prophet'),
            html.Div(className='legenda', children=[
                html.P(children='Media:'),
                html.P(children='Massimo:'),
                html.P(children='Minimo:'),
            ]),
            dcc.Graph(className='grafico', id='bar_plot1', figure=fig2, responsive=True),
        ]),
    ]),
    html.Div(id='image', className='out-container', children=[
        html.Img(src='https://i.ibb.co/8zkNZTT/7VE.gif')
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


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('btn-1', 'n_clicks'),
    Input('btn-2', 'n_clicks'),
    Input('btn-3', 'n_clicks'),
    prevent_initial_call=True
)
def update_graph(btn1, btn2, btn3):
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if btn1 and btn2 and btn3 is None:
        raise PreventUpdate
    else:
        if button_id == 'btn-1':
            trace_1 = go.Scatter(x=dfVax.index, y=dfVax.prima_dose, name='Prima dose', fill='none', connectgaps=True)
            layout = go.Layout(
                legend=dict(
                    yanchor="top",
                    y=0.97,
                    xanchor="left",
                    x=0.01),
                margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
                showlegend=True)
        elif button_id == 'btn-2':
            trace_1 = go.Scatter(x=dfVax.index, y=dfVax.seconda_dose, name='Seconda dose', fill='none',
                                 connectgaps=True)
            layout = go.Layout(
                legend=dict(
                    yanchor="top",
                    y=0.97,
                    xanchor="left",
                    x=0.01),
                margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
                showlegend=True)
        elif button_id == 'btn-3':
            trace_1 = go.Scatter(x=dfVax.index, y=dfVax.dose_addizionale_booster, name='Terza dose ', fill='none',
                                 connectgaps=True)
            layout = go.Layout(
                legend=dict(
                    yanchor="top",
                    y=0.97,
                    xanchor="left",
                    x=0.01),
                margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
                showlegend=True)
        fig4 = go.Figure(data=[trace_1], layout=layout)
        fig4.update_yaxes(type="log")
    return fig4
