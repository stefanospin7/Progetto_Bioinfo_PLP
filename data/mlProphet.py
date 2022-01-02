import pandas as pd
import prophet as Prophet
from functools import reduce
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
Aggiunta MACHINE LEARNING
"""
mlData = ["total_cases", "new_cases", "new_deaths", "new_vaccinations", "people_vaccinated", "people_fully_vaccinated", "total_boosters"]
#mlData = ["total_cases", "new_cases"]



df = pd.read_csv("data/owid-dataset.csv")
df = df.fillna(0)


start_date = df.index.get_level_values(0)[0]
end_date = df.index.get_level_values(0)[-1]
periodo = (df.index.get_level_values(0) >= start_date) & (df.index.get_level_values(0) <= end_date)
nazioni = df['location'].unique().tolist()

#nazioni = ["Italy", "China", "Austria"]


#df = df.set_index(["date", "location"])

df['date'] = df['date'].convert_dtypes(convert_string=True)
df['date'] = pd.to_datetime(df['date'])

df['location'] = df['location'].convert_dtypes(convert_string=True)

#creazione lista colonne comuni
commonCols = []
for i in mlData:
    commonCols.append(i + '_Ml')
    commonCols.append(i + '_MLUp')
    commonCols.append(i + '_MLDw')
print(commonCols)
df[commonCols] = np.nan
commonCols.append('date')
commonCols.append('location')


#days = pd.to_datetime(df.date).dt.date.unique().tolist()
#print(days)
#df = df[df["location"] == "World"]

listForecast = []

#df['date'] = df.index
for naz in nazioni:
    dfN = df[df["location"] == naz]
    print(dfN.head)
    #dfN = df[df.index.get_level_values(1).isin([naz])]
    #dfN = dfN.reset_index()

    #dfN = dfN[dfN.index == days]
    #print(dfN.head(5))
    print(naz)
    dfList = []
    for i in mlData:
        #print(check_for_nan)
        tmp = dfN
        mldt = ["date",i]
        #mldt.append(i)
        tmp = tmp[mldt]
        tmp = tmp[:end_date]
        print(tmp.head(5))


        check_for_nan = tmp[i].isnull().values.any()
        if check_for_nan == True:
            break

        tmp.columns = ['ds', 'y']

        tmp['ds'] = pd.to_datetime(tmp['ds']).dt.date
        # print(dfML.tail())
        m = Prophet.Prophet(weekly_seasonality=True)
        m.fit(tmp)
        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)

        forecast.rename(columns={'ds': 'date','trend': i+'_Ml', 'trend_upper': i+'_MLUp', 'trend_lower': i+'_MLDw'}, inplace=True)
        forecast = forecast[['date', i+'_Ml',i+'_MLUp',i+'_MLDw']]
        forecast['location'] = naz
        globals()["forecast_" + naz + i] = forecast.copy()
        dfList.append(globals()["forecast_" + naz + i])

    print("*************")
    print("Inizio Merge Valori di una nzione")
    print(naz)
    print(dfList)
    print("*************")
    #MERGE valori ML di una nazione
    def merg_Df_i(left, right):
        r = pd.merge(left, right, on=['date', 'location'], suffixes=("", "_y"))
        r.drop(r.filter(regex='_y$').columns.tolist(), axis=1, inplace=True)
        print(r.head(10))
        return r

    globals()["forecast_" + naz] = reduce(lambda df1, df2: merg_Df_i(df1, df2), dfList)
    listForecast.append(globals()["forecast_" + naz])

#MERGE valori ML di tutte le nazioni
print("*************")
print("Inizio Merge Nazioni")
print("*************")



# Funzione per merge di tutti i dataframe di varie nazioni


def merg_Df(left, right):
    print("Tipo sx")
    #print(left.dtypes)
    print(left.head(5))
    print("Tipo dx")
    print(right.dtypes)
    print(right.head(5))
    left['date'] = pd.to_datetime(left['date'])
    #left['iso_code'] = left['iso_code'].apply(pd.to_numeric, downcast='float', errors='coerce')
    right['date'] = pd.to_datetime(right['date'])
    #right['iso_code'] = right['iso_code'].apply(pd.to_numeric, downcast='float', errors='coerce')
    r = pd.merge(left, right, on=(commonCols), suffixes=("", "_y"), how="outer")
    r.drop(r.filter(regex='_y$').columns.tolist(), axis=1, inplace=True)
    print(r.head(10))
    return r

df_merged = reduce(lambda  left,right: merg_Df(left, right), listForecast)
#df_merged = listForecast[0]
dfFinal = pd.merge(df, df_merged, on=('date', 'location'), suffixes=("_x", ""), how="outer")
dfFinal.drop(dfFinal.filter(regex='_x$').columns.tolist(), axis=1, inplace=True)
print(dfFinal.head(10))
print(dfFinal.tail(10))

#listForecast.append(dfo)

#df = df[df["location"] == naz]

dfFinal.to_csv("data/forecast_TOT.csv")

        #print(globals()["forecast_"+naz].head(5))
        #print(listForecast)


   #     df = df.merge(forecast, on=["date", "location"], how="outer")



       # colsD = ['location', 'iso_code', 'latitude', 'longitude']
        #df[df["location"] == naz][colsD] = df[df["location"] == naz][colsD].fillna(method="ffill")
        #print(df[df["location"] == "Zimbabwe"].tail(10))
        #print(df[df["location"] == naz].tail(10))
        #print(df.tail(5))
