"""
Esame PLP
Docente: Prof. Daniele Pasquini
Gruppo 1
Titolo: Analisi dati Covid/Vaccinazioni
Prova 0.2:
- importazione cvs da git hub
- visualizzazione grafico su dash
"""

# pacchetti dash e plotly per visualizzazione


import dash
# pacchetto pandas per leggere e scrivere csv da url
import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from dash import Dash, html, Input, Output, callback_context
from datetime import timedelta, date
import fbprophet as Prophet
from dash.exceptions import PreventUpdate

start_date = "2021-01-01"
end_date = "2021-11-20"

dfDeceduti = pd.read_csv(
    'data/datiCovid.csv',
    index_col='data',
    parse_dates=['data'],  # Intepret the column as a date
    # header=0,
    # relative python path to subdirectory
    # sep='\t'           Tab-separated value file.
    # quotechar="'",        # single quote allowed as quote character
    # dtype={"terapia_intensiva": int},  # Parse the salary column as an integer
    usecols=['data', 'deceduti'],  # Only load the columns specified.
    # skiprows=1,         # Skip the first 10 rows of the file
    # na_values=['.', '??']       # Take any '.' or '??' values as NA
)

dfDeceduti.index = dfDeceduti.index.normalize()

dfVax = pd.read_csv(
    'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv',
    index_col='data_somministrazione',
    parse_dates=['data_somministrazione'],
    # header=0,
    # relative python path to subdirectory
    # sep='\t'           Tab-separated value file.
    # quotechar="'",        # single quote allowed as quote character
    # dtype={"terapia_intensiva": int},  # Parse the salary column as an integer
    # usecols=['data_somministrazione', 'prima_dose', 'seconda_dose'],
    # Only load the three columns specified.
    # parse_dates=['data'],  # Intepret the birth_date column as a date
    # skiprows=1,         # Skip the first 10 rows of the file
    # na_values=['.', '??']       # Take any '.' or '??' values as NA
)

dfDeceduti = dfDeceduti.loc[start_date:end_date]
dfVax = dfVax.loc[start_date:end_date].groupby('data_somministrazione').sum()

dfVaxDeceduti = pd.concat([dfDeceduti, dfVax['prima_dose']], axis=1)

"""
GRAFICO TEST 0.2
"""
fig1 = go.Figure()
# Create and style traces
fig1.add_trace(
    go.Scatter(x=dfVaxDeceduti.index, y=dfVaxDeceduti.prima_dose, name='vaccinati con prima dose', fill='none',
               connectgaps=True))
fig1.add_trace(go.Scatter(x=dfVaxDeceduti.index, y=dfVaxDeceduti.deceduti.diff(), name='deceduti', fill='none'))

fig1.update_yaxes(type="log")  # log range: 10^0=1, 10^5=100000
fig1.update_layout(legend=dict(
    yanchor="top",
    y=0.97,
    xanchor="left",
    x=0.01
),
    margin={'l': 0, 'r': 0, 't': 0, 'b': 0})

"""
MACHINE LEARNING
TEST 0.1
Test redesign dataframe
"""

dfDecedutiML = pd.read_csv(
    'data/datiCovid.csv',
    index_col='data',
    parse_dates=['data'],  # Intepret the column as a date
    # header=0,
    # relative python path to subdirectory
    # sep='\t'           Tab-separated value file.
    # quotechar="'",        # single quote allowed as quote character
    # dtype={"terapia_intensiva": int},  # Parse the salary column as an integer
    usecols=['data', 'deceduti'],  # Only load the columns specified.
    # skiprows=1,         # Skip the first 10 rows of the file
    # na_values=['.', '??']       # Take any '.' or '??' values as NA
)
dfDecedutiML = dfDecedutiML.reset_index()
dfDecedutiML.columns = ['ds', 'y']

dfDecedutiML.ds = dfDecedutiML.ds.dt.date
print(dfDecedutiML.tail())
m = Prophet.Prophet(weekly_seasonality=True)
m.fit(dfDecedutiML)
future = m.make_future_dataframe(periods=365)
forecast = m.predict(future)
print(forecast)
# iterating the columns
for col in forecast.columns:
    print(col)

"""
GRAFICO TEST ML
"""
fig2 = go.Figure()
# Create and style traces
fig2.add_trace(go.Scatter(x=forecast.ds, y=forecast.yhat, name='Test ML Prophet', fill='tonexty', connectgaps=True))
fig2.add_trace(go.Scatter(x=dfDecedutiML.ds, y=dfDecedutiML.y, name='deceduti', fill='tozeroy'))

fig2.update_layout(legend=dict(
    yanchor="top",
    y=0.97,
    xanchor="left",
    x=0.01
),
    margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
    autosize=True
)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=dfVax.index, y=dfVax.prima_dose, name='Prima Dose', fill='none', connectgaps=True))
fig3.update_yaxes(type="log")  # log range: 10^0=1, 10^5=100000
fig3.update_layout(
    legend=dict(
        yanchor="top",
        y=0.97,
        xanchor="left",
        x=0.01),
    margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
    showlegend=True
    )

"""
LAYOUT HTML
"""

app = dash.Dash(__name__,
                title="PLP Project 1 - Bioinformatica Tor Vergata",
                meta_tags=[
                    # A description of the app, used by e.g.
                    # search engines when displaying search results.
                    {
                        'property': 'og:site_name',
                        'content': 'PLP Project 1 - Bioinformatica Tor Vergata',
                    },
                    # A description of the app, used by e.g.
                    # search engines when displaying search results.
                    {
                        'property': 'og:title',
                        'content': 'Progetto di analisi dati Covid-19 e Vaccinazioni',
                    },
                    # A description of the app, used by e.g.
                    # search engines when displaying search results.
                    {
                        'property': 'og:description',
                        'content': 'Progetto di analisi dati Covid-19 e Vaccinazioni',
                    },
{
                        'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0',
                    }
                ],
                )

server = app.server

app.layout = html.Div(id='parent', children=[
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
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if btn1 and btn2 and btn3 is None:
        raise PreventUpdate
    else:
        if button_id == 'btn-1':
            trace_1 = go.Scatter(x=dfVax.index, y=dfVax.prima_dose, name='Prima dose', fill='none',connectgaps=True)
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

if __name__ == '__main__':
    app.run_server(debug=True)
