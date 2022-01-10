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
#settaggio token per accedere a mapbox
px.set_mapbox_access_token(
        "pk.eyJ1IjoibWFuZnJlZG9mcmFjY29sYSIsImEiOiJja3hyd2JjbnEwNnVjMnBvNTZrbHBqdmwzIn0.YFYLdLUxoYC3gSpkcGplqQ")

#lista dati  
datiCol = ["icu_patients", "icu_patients_per_million", "new_cases", "new_cases_per_million", "new_deaths", "new_deaths_per_million", "new_tests", "new_tests_per_thousand", "new_vaccinations", "people_fully_vaccinated", "people_fully_vaccinated_per_hundred", "people_vaccinated", "people_vaccinated_per_hundred", "positive_rate", "total_boosters", "total_boosters_per_hundred", "total_cases", "total_cases_per_million", "total_deaths", "total_deaths_per_million", "total_tests", "total_tests_per_thousand", "total_vaccinations", "total_vaccinations_per_hundred"]
#dizionari per la traduzione dei nomi delle colonne del dataset
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

#lettura globale del csv del dataset owid
dfTot = pd.read_csv("data/owid-dataset.csv",
                    #tratta una stringa come oggetto di tipo data (colonna "date") 
                     parse_dates=["date"]
                     )

"""
CALLBACK PER GRAFICO MONDO
"""

#UPDATE GRAFICO

#@ decorator della libreria che descrive l'input e l'output di default
@app.callback(
    Output("fig-mondo", "figure"),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
)
def update_figMondo(input_dato, start_date, end_date):
    #crea una copia del dataframe globale (per ottimizzare il caricamento del csv)
    df = dfTot

    #elimina le righe in cui la colonna location contiene gli elementi della lista
    locationDel = ['World', 'Asia', 'Africa', 'Oceania', 'Europe', 'High income', 'Low income', 'Upper middle income',
                   'Lower middle income', 'North America', 'South America', 'European Union', 'Qatar']
    df = df[~df.location.isin(locationDel)]

    #definizione del periodo in base all'input utente e filtra il dataframe in base ad esso 
    periodo = (df['date'] >= start_date) & (df['date'] <= end_date)
    df = df.loc[periodo]
    #trasforma la colonna "date" in stringa
    df['date'] = df['date'].dt.date.astype(str)

    #legge il file custom.geo.json che contiene i poligoni delle nazioni 
    with open('data/custom.geo.json') as fp:
        data = json.load(fp)

    #approssima le coordinate a due decimali per alleggerire i calcoli della creazione poligono
    for i in range(0, len(data["features"])):
        for j in range(0, len(data["features"][i]['geometry']['coordinates'])):
            data["features"][i]['geometry']['coordinates'][j] = np.round(
                np.array(data["features"][i]['geometry']['coordinates'][j]), 2)

    
    #definizione grafico choropleth dei dati mondo
    fig = px.choropleth_mapbox(df, #lettura dataframe
                               geojson=data, #lettura geojson per calcolo poligoni nazioni
                               locations='iso_code', #cerca la colonna "iso_code" nel dataframe 
                               color=input_dato, #da il colore al dato
                               featureidkey="properties.iso_a3", #cerca nel geojson il dato iso_a3 che matcha con "iso_code"
                               color_continuous_scale=["rgb(55, 90, 127)", "rgb(0, 188, 140)"], #definisco la scala di colori personalizzata
                               zoom=1, center={"lat": 24.8, "lon": 6.2}, #definisco zoom e la posizione della mappa al caricamento
                               opacity=0.5, 
                               labels={input_dato: dictDati[input_dato]}, 
                               animation_frame='date', #crea un'animazione del grafico in base alla colonna "date"

                               )
    
    #posizionamento corretto dello slider e del play dell'animazione
    fig['layout']['updatemenus'][0]['pad'] = dict(r=10, t=10)
    fig['layout']['sliders'][0]['pad'] = dict(r=10, t=10, )
    #definisce la velocità dell'animazione   
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 50
    #definisce il layout del grafico
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


#UPDATE TITOLO 

@app.callback(
    Output("titolo-mondo", "children"),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
)
#strftime = formatta gli input del range di date nel formato data definito e restituisce l'html con la stringa del dato e del periodo
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
CALLBACK PER SEZIONE CONFRONTO
"""

# UPDATE TITOLO CONFRONTO

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


# TABELLA RIASSUNTIVA DATO 1

@app.callback(
    Output("dati-nazione-1", "children"),
    Input('input-nazione-1', 'value'),
    Input("dato-input-1", "value"),
    Input('date-confronto', 'start_date'),
    Input('date-confronto', 'end_date'),
)
def updateNazione(nazione, dato, start_date, end_date):
    #istanzio la classe analisi passando nazione e il dataframe tot come parametro a costruttore 
    #.df mi fa accedere al filtro per il valore nazione creato dal costruttore 
    df = Analisi(nazione, dfTot).df
    periodo = (df["date"] > start_date) & (df["date"] <= end_date)
    datiCol = [dato]
    df = df[datiCol]
    df = df.loc[periodo]
    titDato = dictDati[dato] + " - " + nazione
    outputNazione = dbc.ListGroup(
        [
            #visualizzo titolo del dato 1 nel layout html di output
            dbc.ListGroupItem(titDato,
                              color="primary",
                              className="bg-info"
                              ),
            #elaboro media, massimo, minimo e le visualizzo 
            dbc.ListGroupItem(["Media", dbc.Badge(round(df[dato].mean(), 2), color="light", text_color="primary", className="ms-1"),],color="primary"),
            dbc.ListGroupItem(["Minimo", dbc.Badge(df[dato].min(), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),
            dbc.ListGroupItem(["Massimo", dbc.Badge(df[dato].max(), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),

        ]
    )
    return outputNazione


# TABELLA RIASSUNTIVA DATO 2 

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
            dbc.ListGroupItem(["Media", dbc.Badge(round(df[dato].mean(), 2), color="light", text_color="primary", className="ms-1"),],color="primary"),
            dbc.ListGroupItem(["Minimo", dbc.Badge(df[dato].min(), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),
            dbc.ListGroupItem(["Massimo", dbc.Badge(df[dato].max(), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),

        ]
    )
    return outputNazione


# GRAFICO CONFRONTO

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
  #funzione per istanziare la classe Analisi e filtrarla in base ai valori di input di nazione e dato
    def generateDf(nazione, dato):
        df = Analisi(nazione, dfTot).df
        periodo = (df["date"] > start_date) & (df["date"] <= end_date)
        datiCol = ["date", dato]
        df = df[datiCol]
        df = df.loc[periodo]
        return df

    df1 = generateDf(nazione1, datoInputOne)
    df2 = generateDf(nazione2, datoInputTwo)

    # Crea il grafico
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
CALLBACK PER SEZIONE MACHINE LEARNING
"""

#UPDATE TITOLO MACHINE LEARNING

@app.callback(
    Output("titolo-ML", "children"),
    Input("dato-input-ML", "value"),
    Input("input-nazione-ML", "value"),
)
def updateTitML(dato, nazione):
    #istanzio la classe analisi definendo i parametri del costruttore filtrndo il dataframe
    df = Analisi(nazione, dfTot).df
    #iloc = seleziona l'indice del dataframe filtrato
    inizio = df["date"].iloc[0].strftime("%d/%m/%Y")
    fine = df["date"].iloc[-1].strftime("%d/%m/%Y")
    periodo = "Trend: " + inizio + " - " + fine + " | Proiezione: 100 giorni"
    #dictDati = variabile globale. [dato] è la chiave del dizionario (chiave : valore )
    #dictDati[dato] restituisce il valore in dictDati corrispondente alla chiave “dato”
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
    #restituisce quello che c'è dentro dbc.Row
    return x

# GRAFICO ML 

@app.callback(
    Output("fig-ML", "figure"),
    Input('dato-input-ML', 'value'),
    Input('input-nazione-ML', 'value'),
)
def updateFigML(dato_input, nazione):
    #scikit learn
    from datetime import date as dt
    data = dfTot
    #filtro il df e prendo solo le righe con la voce nazione
    data = data[data["location"] == nazione]
    import numpy as np
    #np.inf = va a sostituire gli infiniti con uno 0
    #fillna = va a rimpiazzare il valore nan con 0
    data = data.fillna(0).replace(np.inf, 0) 
    dates = data['date']
    #d =variabile che va ad indicare “ per ogni”
    #for d in dates è iterabile ovvero posso iterare sulle sue righe 
    #prendo le date che si trovano dentro la serie dates e le converto in datetime
    date_format = [pd.to_datetime(d) for d in dates]


    # preparo il modello
    X = date_format
    #tolist = trasforma una serie in una lista
    #[1:] toglie il primo elemento perché inizia dall’indice 1
    y = data[dato_input].tolist()[1:]

    starting_date = 1  
    day_numbers = []
    for i in range(1, len(X)):
        day_numbers.append([i])
    X = day_numbers
    #vengono tolti i primi elemnti ad X ed Y fino al numero starting_date
    X = X[starting_date:]
    y = y[starting_date:]
    #viene istanziata la classe linear_regr (la regressione lineare approssima l'andamento del grafico con una retta)
    linear_regr = linear_model.LinearRegression()

    #fit = facciamo il training set del modello 
    linear_regr.fit(X, y)
    #predict ritorna valori predetti 
    y_pred = linear_regr.predict(X)
    #tiene in considerazione gli errori massimi e minimi per il modello della predizione 
    error = max_error(y, y_pred)
    #comprende sia gli indici dei dati di origine che quelli di proiezione 
    X_test = []
    future_days = 1000
    for i in range(starting_date, starting_date + future_days):
        X_test.append([i])
    
    #elabora i valori effettivi della predizione 
    y_pred_linear = linear_regr.predict(X_test)
    #considera gli errori massimi e minimi di predizione commessi dal modello
    y_pred_max = []
    y_pred_min = []
    for i in range(0, len(y_pred_linear)):
        y_pred_max.append(y_pred_linear[i] + error)
        y_pred_min.append(y_pred_linear[i] - error)
    
    #zip e list = prende quattro liste e restituisce un'unica lista ordinata in base agli indici di partenza
    new_df = pd.DataFrame(list(zip(X_test, y_pred_max, y_pred_min, y_pred_linear)),
                          columns=['indice', 'massimo', "minimo", "predictions"])

    nuovo_indice = []
    date_indicizzate = []
    #crea una colonna che trasforma gli indici in date 
    date_time_str = "2020-04-01"
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d') + timedelta(days=1)
    for i in range(0, len(new_df.indice)):
        nuovo_indice.append(new_df.indice[i][0])
        date_indicizzate.append(date_time_obj + timedelta(days=i))
    new_df["indice"] = date_indicizzate

    #prophet
    #istanzio una copia del df filtrata per il dato di input 
    tmp = data
    keep = ["date", dato_input]
    tmp = tmp[keep]
    #rinomina le colonne del df come "ds"(data) e "y"(valori) come richiesto da prophet
    tmp.columns = ['ds', 'y']
    #converte la data nel formato datetamp
    tmp['ds'] = pd.to_datetime(tmp['ds']).dt.date
    #istanzio oggetto prophet con stagionalità settimanale
    m = Prophet.Prophet(weekly_seasonality=True)
    #fit = facciamo il training set del modello
    m.fit(tmp)
    #include le date della storia per andare a creare il modello
    future = m.make_future_dataframe(periods=365)
    #elabora i dati futuri
    forecast = m.predict(future)
    
    #grafico di sintesi ML regressione lineare e prophet
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
