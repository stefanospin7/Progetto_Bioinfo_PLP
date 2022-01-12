import pandas as pd
# owid dataset import 
df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
                 parse_dates=["date"])
# keep = select columns of interest
keep = ["date", "location", "iso_code", "icu_patients", "icu_patients_per_million", "new_cases", "new_cases_per_million", "new_deaths", "new_deaths_per_million", "new_tests", "new_tests_per_thousand", "new_vaccinations", "people_fully_vaccinated", "people_fully_vaccinated_per_hundred", "people_vaccinated", "people_vaccinated_per_hundred", "positive_rate", "total_boosters", "total_boosters_per_hundred", "total_cases", "total_cases_per_million", "total_deaths", "total_deaths_per_million", "total_tests", "total_tests_per_thousand", "total_vaccinations", "total_vaccinations_per_hundred"]
df = df[keep]
# to_csv exporting filtered csv  
df.to_csv("data/owid-dataset.csv")
