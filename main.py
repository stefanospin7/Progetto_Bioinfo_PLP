"""
Esame PLP
Docente: Prof. Daniele Pasquini
Gruppo 1
Titolo: Analisi dati Covid/Vaccinazioni
Prova 0.2:
- importazione cvs da git hub
- visualizzazione grafico su dash
"""


"""
# pacchetto pandas per leggere e scrivere csv da url
import pandas as pd

# pacchetti dash e plotly per visualizzazione
import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash()

df = pd.read_csv(
            'data/datiCovid.csv',
            # index_col='data',
            parse_dates=['data'],
            # header=0,
            # relative python path to subdirectory
            # sep='\t'           Tab-separated value file.
            # quotechar="'",        # single quote allowed as quote character
            # dtype={"terapia_intensiva": int},  # Parse the salary column as an integer
            # usecols=['data', 'ricoverati_con_sintomi', 'terapia_intensiva', 'totale_ospedalizzati'],
            # Only load the three columns specified.
            # parse_dates=['data'],  # Intepret the birth_date column as a date
            # skiprows=1,         # Skip the first 10 rows of the file
            # na_values=['.', '??']       # Take any '.' or '??' values as NA
        )

dfVax = pd.read_csv(
            'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv',
            # index_col='data',
            parse_dates=['data_somministrazione'],
            # header=0,
            # relative python path to subdirectory
            # sep='\t'           Tab-separated value file.
            # quotechar="'",        # single quote allowed as quote character
            # dtype={"terapia_intensiva": int},  # Parse the salary column as an integer
            # usecols=['data', 'ricoverati_con_sintomi', 'terapia_intensiva', 'totale_ospedalizzati'],
            # Only load the three columns specified.
            # parse_dates=['data'],  # Intepret the birth_date column as a date
            # skiprows=1,         # Skip the first 10 rows of the file
            # na_values=['.', '??']       # Take any '.' or '??' values as NA
        )


fig = go.Figure()
# Create and style traces
fig.add_trace(go.Scatter(x=df.data, y=df.totale_ospedalizzati, name='totale_ospedalizzati',
                         ))
fig.add_trace(go.Scatter(x=df.data, y=df.ricoverati_con_sintomi, name='ricoverati_con_sintomi',
                         ))
fig.add_trace(go.Scatter(x=df.data, y=df.terapia_intensiva, name='terapia_intensiva',
                         ))
fig.add_trace(go.Scatter(x=dfVax.data_somministrazione, y=dfVax.prima_dose, name='prima_dose',
                         ))
start_date = "2021-03-26"
end_date = "2021-10-18"

fig.update_xaxes(type="date", range=[start_date, end_date])

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'title', children = 'Esame PLP'),
    html.H2(id = 'docente', children = 'Docente: Prof. Daniele Pasquini'),
    html.H3(id = '', children = 'Gruppo 1'),
    html.H2(id = '', children = 'Titolo: Analisi dati Covid/Vaccinazioni'),

    dcc.Graph(id = 'bar_plot', figure = fig)
    ])

if __name__ == '__main__':
    def app(environ, start_response):
        data = b"Hello, World!\n"
        start_response("200 OK", [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data])
    app.run_server()"""







