"""
Pull data from database and export an aggregated .cvs file
"""
# pacchetto pandas per leggere e scrivere csv da url
import pandas as pd
# pacchetto datetime per utilizzo e manipolaizione date
from datetime import timedelta, date
# pacchetto plotly.express per visualizzazione grafici
import plotly.express as px

# definisco procedura range di date
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# definisco data di inizio e fine dell'analisi dati
start_date = date(2020, 2, 24)
end_date = date.today()

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
        ))
    i = i + 1
# ho concatenato in un data frame pandas gli elementi della lista data[]
df = pd.concat(data)
df.to_csv('data/datiCovid.csv', index=False)
#print(df)
# visualizzo una colonna del dataframe in grafico su dash
#fig = px.line(df, x="data", y="totale_ospedalizzati", title="Ricoverati COVID")
#fig.show()








