"""
Pull data from database and export an aggregated .cvs file
"""

from datetime import timedelta, date # pacchetto datetime per utilizzo e manipolaizione date
import pandas as pd  # gestione csv/dataframe
import fbprophet as Prophet # machine learning fbprophet


"""
definisco data di inizio dell'analisi dati  e termine alla data di oggi
"""
start_date = date(2020, 2, 24)
end_date = date.today()

"""
Scarico il dataset COVID Andamento nazionale
"""

# definisco procedura range di date per l'iterazione per unire i csv di ogni giorno presenti sul repo della Protezione civile
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# inizializzo e popolo lista di indirizzi url dei file cvs su git-hub
indirizzi = []
for n in daterange(start_date, end_date):
    indirizzi.append(("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-" + n.strftime("%Y%m%d") + ".csv"))
#print(indirizzi)
# inizializzo e popolo dataframe tramite pandas selezionando specifiche colonne dei file cvs
data = []
i = 0
for n in indirizzi:
    data.append(
        pd.read_csv(
            indirizzi[i],
            index_col='data',
            parse_dates=['data'],
            usecols=['data','totale_positivi','variazione_totale_positivi','nuovi_positivi','totale_ospedalizzati','deceduti','ricoverati_con_sintomi','terapia_intensiva','ingressi_terapia_intensiva','tamponi'],
        ))
    i = i + 1

# concateno in un data frame pandas gli elementi della lista data[]
dfCvIt = pd.concat(data)
dfCvIt = dfCvIt.groupby('data').max()
dfCvIt.index = dfCvIt.index.normalize()

"""
Aggiunta MACHINE LEARNING
"""
dfML = dfCvIt[["deceduti"]]
dfML = dfML.reset_index()
dfML.columns = ['ds', 'y']
dfML.ds = dfML.ds.dt.date
#print(dfML.tail())
m = Prophet.Prophet(weekly_seasonality=True)
m.fit(dfML)
future = m.make_future_dataframe(periods=365)
forecast = m.predict(future)
#print(forecast)
# iterating the columns
#for col in forecast.columns:
#    print(col)
forecast.index = forecast['ds']
forecast.index = pd.to_datetime(forecast.index)
#print(forecast.tail(10))
forecast.rename(columns={'trend': 'decedutiMl', 'trend_upper': 'decedutiMLUp', 'trend_lower': 'decedutiMLDw'}, inplace=True)
forecast = forecast[['decedutiMl','decedutiMLUp','decedutiMLDw']]
dfCvMLIt = pd.concat([dfCvIt, forecast], axis=1) # concatena 2 dataframe

#creo file cvs in cartella /data
dfCvMLIt.to_csv('data/datiCovidItalia.csv', index=True)

"""
Scarico il dataset Vaccini Italia
"""

dfVaxIt = pd.read_csv(
    'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv',
    index_col='data_somministrazione',
    parse_dates=['data_somministrazione'],
    usecols=['data_somministrazione','fornitore','fascia_anagrafica','prima_dose','seconda_dose','dose_addizionale_booster'],
)
dfVaxIt.rename(columns={'data_somministrazione': 'data'}, inplace=True)
#creo file cvs in cartella /data
dfVaxIt.to_csv('data/datiVacciniItalia.csv', index=True)

