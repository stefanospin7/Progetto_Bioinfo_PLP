import pandas as pd  # gestione csv/dataframe
import plotly.graph_objects as go  # creazione grafici
import fbprophet as Prophet # machine learning fbprophet

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
    usecols=['data_somministrazione', 'prima_dose', 'seconda_dose'],
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
