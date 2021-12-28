import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
                 parse_dates=["date"])
# df = df[df["location"] == "World"]
keep = ["location", "date", "total_cases", "new_cases", "icu_patients", "new_deaths", "hosp_patients", "new_tests",
        "new_vaccinations", "people_vaccinated", "people_fully_vaccinated", "total_boosters", "iso_code"]
df = df[keep]
df.to_csv("data/owid-dataset.csv")
print(df.head())
