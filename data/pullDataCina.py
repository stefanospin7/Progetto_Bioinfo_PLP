import pandas as pd

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv",
                 usecols=["date", "location", "total_cases", "new_cases", "icu_patients", "new_deaths", "hosp_patients", "new_tests"],
                 index_col="date",
                 parse_dates=["date"])
df = df.loc[df["location"] == "China"]
df = df.drop("location", axis=1)
df.rename(columns={'date': 'data', 'total_cases': 'totale_positivi', 'new_cases' : 'nuovi_positivi', 'icu_patients' : 'terapia_intensiva', 'new_deaths' : 'deceduti', 'hosp_patients' : 'totale_ospedalizzati', 'new_tests' : 'tamponi'}, inplace=True)
df.index.names = ['data']
print(df.tail(10))

df.to_csv("datiCovidCina.csv", index=True)
