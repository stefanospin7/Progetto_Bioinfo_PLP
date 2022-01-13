import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#import dash app 
from appCovidData.app import app
from dash import Input, Output, State  
from dash import html  
import dash_bootstrap_components as dbc
#import classeAnalisi
from appCovidData.classeAnalisi import Analisi
import numpy as np
from datetime import datetime, timedelta, date
from sklearn import linear_model
from sklearn.metrics import max_error
import prophet as Prophet
import json
import math
import locale
from decimal import Decimal
locale.setlocale(locale.LC_ALL, 'en_US')

# setting token to access mapbox 
px.set_mapbox_access_token(
        "pk.eyJ1IjoibWFuZnJlZG9mcmFjY29sYSIsImEiOiJja3hyd2JjbnEwNnVjMnBvNTZrbHBqdmwzIn0.YFYLdLUxoYC3gSpkcGplqQ")

# data list   
datiCol = ["icu_patients", "icu_patients_per_million", "new_cases", "new_cases_per_million", "new_deaths", "new_deaths_per_million", "new_tests", "new_tests_per_thousand", "new_vaccinations", "people_fully_vaccinated", "people_fully_vaccinated_per_hundred", "people_vaccinated", "people_vaccinated_per_hundred", "positive_rate", "total_boosters", "total_boosters_per_hundred", "total_cases", "total_cases_per_million", "total_deaths", "total_deaths_per_million", "total_tests", "total_tests_per_thousand", "total_vaccinations", "total_vaccinations_per_hundred"]
# dictionaries to translate ddataset columns' names 
dictDati = {
"icu_patients" : "Terapia Intensiva",
"icu_patients_per_million" : "Terapia Intensiva per milione",
"new_cases" : "Casi giornalieri",
"new_cases_per_million" : "Casi giornalieri per milione",
"new_deaths" : "Decessi giornalieri",
"new_deaths_per_million" : "Decessi giornalieri per milione",
"new_tests" : "Tamponi giornalieri",
"new_tests_per_thousand" : "Tamponi per centinaia",
"new_vaccinations" : "Vaccinazioni giornaliere",
"people_fully_vaccinated" : "Vaccinati completamente",
"people_fully_vaccinated_per_hundred" : "Vaccinati completamente per centinaia",
"people_vaccinated" : "Vaccinati totali",
"people_vaccinated_per_hundred" : "Vaccinati totali per centinaia",
"positive_rate" : "Tasso di positività",
"total_boosters" : "Dosi booster totali",
"total_boosters_per_hundred" : "Dosi booster totali per centinaia",
"total_cases" : "Casi totali",
"total_cases_per_million" : "Casi totali per milione",
"total_deaths" : "Decessi totali",
"total_deaths_per_million" : "Decessi totali per milione",
"total_tests" : "Tamponi totali",
"total_tests_per_thousand" : "Tamponi totali per migliaia",
"total_vaccinations" : "Dosi somministrate totali",
"total_vaccinations_per_hundred" : "Dosi somministrate per centiania",
}

# global read_csv of owid dataset 
dfTot = pd.read_csv("data/owid-dataset.csv",
                    # processing a string as a date-time object type (column "date") 
                     parse_dates=["date"]
                     )

"""
WORLD DATA GRAPH CALLBACK
"""

# GRAPH UPDATE

#@ decorator of the library which describes the default of input and output 
@app.callback(
    Output("fig-mondo", "figure"),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
)
def update_figMondo(input_dato, start_date, end_date):
    # creating a copy of the global dataframe (to optimize the csv loading) 
    df = dfTot

    # deleting rows in which location column contains some elements of the list  
    locationDel = ['World', 'Asia', 'Africa', 'Oceania', 'Europe', 'High income', 'Low income', 'Upper middle income',
                   'Lower middle income', 'North America', 'South America', 'European Union', 'Qatar']
    df = df[~df.location.isin(locationDel)]

    # definition of the time period and filtering of dataframe according to the user input 
    periodo = (df['date'] >= start_date) & (df['date'] <= end_date)
    df = df.loc[periodo]
    # convert the column "date" into a string 
    df['date'] = df['date'].dt.date.astype(str)

    # reading the file custom.geo.json which contains polygons of the Nations
    with open('data/custom.geo.json') as fp:
        data = json.load(fp)

    # rounding (approssima) coordinates to two decimals to optimize the calculation to create polyogons  
    for i in range(0, len(data["features"])):
        for j in range(0, len(data["features"][i]['geometry']['coordinates'])):
            data["features"][i]['geometry']['coordinates'][j] = np.round(
                np.array(data["features"][i]['geometry']['coordinates'][j]), 2)

    
    # defying choropleth graph of the World data 
    fig = px.choropleth_mapbox(df, # dataframe reading
                               geojson=data, # geojson reading to calculate polygons of Nations 
                               locations='iso_code', # searching the column "iso_code" in dataframe 
                               color=input_dato, # giving to data the color
                               featureidkey="properties.iso_a3", # searching in geojson the data iso_a3 which matches with "iso_code"
                               color_continuous_scale=["rgb(55, 90, 127)", "rgb(0, 188, 140)"], # defying the personalized color scale 
                               zoom=1, center={"lat": 24.8, "lon": 6.2}, # defying map zoom and position at the page loading 
                               opacity=0.5, 
                               labels={input_dato: dictDati[input_dato]}, 
                               animation_frame='date', # creating a graph animation according to the column "date"

                               )
    
    # correct placing of the animation slider and play 
    fig['layout']['updatemenus'][0]['pad'] = dict(r=10, t=10)
    fig['layout']['sliders'][0]['pad'] = dict(r=10, t=10, )
    # defying animation speed   
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 50
    # defying graph layout
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#fff',
        legend=dict(
            yanchor="top",
            y=0.97,
            xanchor="left",
            bgcolor="Black",
            x=0.01),
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        showlegend=True,
        coloraxis_colorbar=dict(
            title="",
        )
        )
    return fig


# TITLE UPDATE 

@app.callback(
    Output("titolo-mondo", "children"),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
)
#strftime = formats input of dates range into defined data format and returns html with a string containing data and period  
def updateTitDato(dato, start_date, end_date): 
    inizio = pd.to_datetime(start_date).strftime("%d/%m/%Y")
    fine = pd.to_datetime(end_date).strftime("%d/%m/%Y")
    periodo = inizio + " - " + fine
    x = dbc.Row([
        dbc.Col(html.H3(children=dictDati[dato], className="fs-4 m-0"),
                width=12,
                md=6),
        dbc.Col(html.P(children= periodo, className="text-md-end m-0"),
                width=12,
                md=6)
                 ],
    )
    return x
  
"""
"FAI UN CONFRONTO" SECTION CALLBACK 
"""

# "CONFRONTO" TITLE UPDATE

@app.callback(
    Output("titolo-confronto", "children"),
    Input("dato-input-1", "value"),
    Input("dato-input-2", "value"),
    Input("input-nazione-1", "value"),
    Input("input-nazione-2", "value"),
    Input('date-confronto', 'start_date'),
    Input('date-confronto', 'end_date'),
)
def updateTitConfronto(dato1, dato2, nazione1, nazione2, start_date, end_date):
    inizio = pd.to_datetime(start_date).strftime("%d/%m/%Y")
    fine = pd.to_datetime(end_date).strftime("%d/%m/%Y")
    periodo = inizio + " - " + fine
    titDato = dictDati[dato1] + " - " + nazione1 + " vs " + dictDati[dato2] + " - " + nazione2
    x = dbc.Row([
        dbc.Col(html.H3(children= titDato, className="fs-4 m-0"),
                width=12,
                md=6),
        dbc.Col(html.P(children= periodo, className="text-md-end m-0"),
                width=12,
                md=6)
                 ],
    )
    return x


# SUM TABLE DATO 1

@app.callback(
    Output("dati-nazione-1", "children"),
    Input('input-nazione-1', 'value'),
    Input("dato-input-1", "value"),
    Input('date-confronto', 'start_date'),
    Input('date-confronto', 'end_date'),
)
def updateNazione(nazione, dato, start_date, end_date):
    # stating analysis class giving as parameter to constructor "Nation" and the total dataframe
    #.df gives me the access to the filter for the Nation value created by the constructor
    df = Analisi(nazione, dfTot).df
    periodo = (df["date"] > start_date) & (df["date"] <= end_date)
    datiCol = [dato]
    df = df[datiCol]
    df = df.loc[periodo]
    titDato = dictDati[dato] + " - " + nazione
    outputNazione = dbc.ListGroup(
        [
            # displaying data 1 title in the layout html output 
            dbc.ListGroupItem(titDato,
                              color="primary",
                              className="bg-info"
                              ),
            # elaborating and displaying  mean, max, min
            dbc.ListGroupItem(["Media", dbc.Badge(locale.format_string('%.2f', round(df[dato].mean(), 2), grouping = True), color="light", text_color="primary", className="ms-1"),],color="primary"),
            dbc.ListGroupItem(["Minimo", dbc.Badge(locale.format_string('%.0f', df[dato].min(), grouping = True), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),
            dbc.ListGroupItem(["Massimo", dbc.Badge(locale.format_string('%.0f', df[dato].max(), grouping = True), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),

        ]
    )
    return outputNazione


#  DATA 2 SUM TABLE  

@app.callback(
    Output("dati-nazione-2", "children"),
    Input('input-nazione-2', 'value'),
    Input("dato-input-2", "value"),
    Input('date-confronto', 'start_date'),
    Input('date-confronto', 'end_date'),
)
def updateNazione(nazione, dato, start_date, end_date):
    df = Analisi(nazione, dfTot).df
    periodo = (df["date"] > start_date) & (df["date"] <= end_date)
    datiCol = [dato]
    df = df[datiCol]
    df = df.loc[periodo]
    titDato = dictDati[dato] + " - " + nazione
    outputNazione = dbc.ListGroup(
        [
            dbc.ListGroupItem(titDato,
                              color="primary",
                              className="bg-success"),
            dbc.ListGroupItem(["Media", dbc.Badge(locale.format_string('%.2f', round(df[dato].mean(), 2), grouping = True), color="light", text_color="primary", className="ms-1"),],color="primary"),
            dbc.ListGroupItem(["Minimo", dbc.Badge(locale.format_string('%.0f', df[dato].min(), grouping = True), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),
            dbc.ListGroupItem(["Massimo", dbc.Badge(locale.format_string('%.0f', df[dato].max(), grouping = True), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),

        ]
    )
    return outputNazione


# "CONFRONTO" GRAPH 

@app.callback(
    Output("fig-confronto", "figure"),
    Input('input-nazione-1', 'value'),
    Input('input-nazione-2', 'value'),
    Input("dato-input-1", "value"),
    Input("dato-input-2", "value"),
    Input('date-confronto', 'start_date'),
    Input('date-confronto', 'end_date'),
)
def updateFigConfronto(nazione1, nazione2, datoInputOne, datoInputTwo, start_date, end_date):
  # function to state analysis class and filter it according to input values  of the Nation and data 
    def generateDf(nazione, dato):
        df = Analisi(nazione, dfTot).df
        periodo = (df["date"] > start_date) & (df["date"] <= end_date)
        datiCol = ["date", dato]
        df = df[datiCol]
        df = df.loc[periodo]
        return df

    df1 = generateDf(nazione1, datoInputOne)
    df2 = generateDf(nazione2, datoInputTwo)

    # creating the graph 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1["date"], y=df1[datoInputOne], name=dictDati[datoInputOne] + " - " + nazione1, fill='tonexty', connectgaps=True, line_color="rgb(52, 152, 219)"))
    fig.add_trace(go.Scatter(x=df2["date"], y=df2[datoInputTwo], name=dictDati[datoInputTwo] + " - " + nazione2, fill='tonexty', connectgaps=True, line_color="rgb(0, 188, 140)"))
    fig.update_yaxes(type="log")
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#fff',
        legend=dict(
            yanchor="top",
            y=0.97,
            xanchor="left",
            bgcolor="Black",
            x=0.01),
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        showlegend=True
    )
    fig.update_xaxes(range=[start_date, end_date])
    return fig

"""
MACHINE LEARNING SECTION CALLBACK 
"""

# MACHINE LEARNING TITLE UPDATE

@app.callback(
    Output("titolo-ML", "children"),
    Input("dato-input-ML", "value"),
    Input("input-nazione-ML", "value"),
)
def updateTitML(dato, nazione):
    # stating analysis class defying parameters of the constructor and filtering the dataframe 
    df = Analisi(nazione, dfTot).df
    #iloc = selects filtered dataframe index 
    inizio = df["date"].iloc[0].strftime("%d/%m/%Y")
    fine = df["date"].iloc[-1].strftime("%d/%m/%Y")
    periodo = "Trend: " + inizio + " - " + fine + " | Proiezione: 365 giorni"
    #dictDati = global variable. [dato] is the key of the dictionary (key : values)
    #dictDati[dato] return the value into dictDati which corresponds to the key  “dato”
    titDato = dictDati[dato] + " - " + nazione
    x = dbc.Row([
        dbc.Col(html.H3(children= titDato, className="fs-4 m-0"),
                width=12,
                md=6),
        dbc.Col(html.P(children= periodo, className="text-md-end m-0"),
                width=12,
                md=6)
                 ],
    )
    # returning what is inside dbc.Row
    return x

# ML GRAPH

@app.callback(
    Output("fig-ML", "figure"),
    Input('dato-input-ML', 'value'),
    Input('input-nazione-ML', 'value'),
)
def updateFigML(dato_input, nazione):
    #scikit learn

    data = dfTot
    # filtering the df and considering only the rows with the value of the corresponding Nation 
    data = data[data["location"] == nazione]

    #np.inf = replaces infinity values with a 0
    #fillna = replaces nan with 0
    data = data.fillna(0).replace(np.inf, 0) 
    dates = data['date']
    #d =variable which indicates “for each”
    #for d in dates can be iterated  and can be iterated for its rows  
    # taking the dates inside dates' series and  converting them into datetime 
    date_format = [pd.to_datetime(d) for d in dates]


    # preparing the model 
    X = date_format
    #tolist =  converts a series into a list 
    #[1:] removes the first element beacuse it starts from index 1
    y = data[dato_input].tolist()[1:]

    starting_date = 0
    day_numbers = []
    for i in range(1, len(X)):
        day_numbers.append([i])
    X = day_numbers
    # removing the first elements for X and Y up to the numbers starting_date
    X = X[starting_date:]
    y = y[starting_date:]
    # stating the class linear_regr (linear regression approximates the graph trend with a line)
    linear_regr = linear_model.LinearRegression()

    #fit = do the training set of the model
    linear_regr.fit(X, y)
    # predict return the predicted values  
    y_pred = linear_regr.predict(X)
    # considering the maximun and minumum errors resulting from the predictive model 
    error = max_error(y, y_pred)
    # includes both indexes of native data and the predictive ones   
    X_test = []
    future_days = len(X) + 365
    for i in range(starting_date, starting_date + future_days):
        X_test.append([i])
    
    # elaborate the actual values for the prediction 
    y_pred_linear = linear_regr.predict(X_test)
    # considering the maximun and minumum errors resulting from the predictive model
    y_pred_max = []
    y_pred_min = []
    for i in range(0, len(y_pred_linear)):
        y_pred_max.append(y_pred_linear[i] + error)
        y_pred_min.append(y_pred_linear[i] - error)
    
    #zip e list = takes four lists and return a single organized list according to the starting indexes
    new_df = pd.DataFrame(list(zip(X_test, y_pred_max, y_pred_min, y_pred_linear)),
                          columns=['indice', 'massimo', "minimo", "predictions"])

    date_indicizzate = []
    # creates a column that converts indexes into dates  
    date_time_str = date_format[0]
    #date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d') + timedelta(days=0)
    for i in range(0, len(new_df.indice)):
        date_indicizzate.append(date_time_str + timedelta(days=i))
    new_df["indice"] = date_indicizzate

    #prophet
    # stating a copy of the filtered df for the input data 
    tmp = data
    # converting the dates into datetamp format
    tmp['date1'] = pd.to_datetime(tmp['date']).dt.date
    keep = ["date1", dato_input]
    tmp = tmp[keep]
    # renaming columns of the df as "ds"(dates) e "y"(values) as it is required by prophet
    tmp.columns = ['ds', 'y']

    # stating prophet object with a weekly seasonality (rate)
    m = Prophet.Prophet(weekly_seasonality=True)
    #fit = doing training set of the model 
    m.fit(tmp)
    # considering  the dates of the history to create the model 
    future = m.make_future_dataframe(periods=365)
    #elaborating future data 
    forecast = m.predict(future)
    
    # ML sum graph linear regression and prophet
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=data["date"], y=data[dato_input], name=dictDati[dato_input] + " - " + nazione, connectgaps=True,
                   fill='tozeroy', line_color = "rgb(55, 90, 127)"))
    fig.add_trace(go.Scatter(x=new_df.indice, y=new_df["predictions"],
                             name=dictDati[dato_input] + " Machine Learning SciKit Learn" + " - " + nazione,
                             connectgaps=True, line_color = "rgb(52, 152, 219)"))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"],
                             name=dictDati[dato_input] + " Machine Learning Prophet" + " - " + nazione,
                             connectgaps=True, line_color = "rgb(0, 188, 140)"))
    
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#fff',
        legend=dict(
            yanchor="top",
            y=0.97,
            xanchor="left",
            bgcolor="Black",
            x=0.01),
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        showlegend=True
    )
    return fig
