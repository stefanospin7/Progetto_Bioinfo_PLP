import pandas as pd
import matplotlib.pyplot as plt

vaccini_globali = pd.read_csv("data/global_vaccinations.csv", parse_dates=["date"])
vaccini_globali = vaccini_globali[vaccini_globali["location"] == "World"]
keep = ["location", "date", "daily_vaccinations", "people_vaccinated", "people_fully_vaccinated", "total_boosters"]
vaccini_globali = vaccini_globali[keep]
vaccini_globali = vaccini_globali.rename(columns={"date": "data", "location": "paese",
                                                  "daily_vaccinations": "vaccinazioni"})
vaccini_globali.to_csv("data/vaccini_globali.csv")
print(vaccini_globali.head())
