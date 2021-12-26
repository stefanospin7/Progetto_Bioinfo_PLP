"""DATI COVID
data
totale_positivi
variazione_totale_positivi
nuovi_positivi
totale_ospedalizzati
deceduti
ricoverati_con_sintomi
terapia_intensiva
ingressi_terapia_intensiva
tamponi """

#import di pandas
import pandas as pd
df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv",
                 usecols=["date", "total_cases", "new_cases", "icu_patients", "new_deaths", "hosp_patients", "new_tests"],
                 index_col="date",
                 parse_dates=["date"])
df = df.groupby(['date']).sum() #funzione che raggruppa le date e mi fa la somma
df.rename(columns={'date': 'data', 'total_cases': 'totale_positivi', 'new_cases' : 'nuovi_positivi', 'icu_patients' : 'terapia_intensiva', 'new_deaths' : 'deceduti', 'hosp_patients' : 'totale_ospedalizzati', 'new_tests' : 'tamponi'}, inplace=True)
print(df.tail(10)) #stampa le prime 10 righe dell'head (parte iniziale) o tail del dataframe
df.to_csv('data/datiCovidMondo.csv')
