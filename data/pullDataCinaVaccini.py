"""DATI VACCINI
Data
fornitore
fascia_anagrafica
prima_dose
seconda_dose
dose_addizionale_booster"""
"""
location
iso_code
date
total_vaccinations
people_vaccinated
people_fully_vaccinated
total_boosters
daily_vaccinations_raw
daily_vaccinations
total_vaccinations_per_hundred
people_vaccinated_per_hundre
people_fully_vaccinated_per_hundred
total_boosters_per_hundred
daily_vaccinations_per_million
daily_people_vaccinated
daily_people_vaccinated_per_hundredé"""



import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv",
                 index_col="date",
                 parse_dates=["date"],
                 usecols=["date", "location","daily_vaccinations","total_boosters", "total_vaccinations"]
                 )
df = df[df["location"] == "China"]




df=df.drop(["location"], axis=1)
df.rename(columns={'date': 'data', "daily_vaccinations":"nuovi_vaccinati","total_boosters":"terza_dose", "total_vaccinations":"vaccinazioni_totali"}, inplace=True)
print(df.tail(10))

df.to_csv("datiVacciniCina.csv", index=True)