import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from appCovidData.app import app
from dash import Input, Output, State  # funzioni di layout html interattivo
import time
from dash import html  # funzioni di layout html interattivo
import dash_bootstrap_components as dbc
from appCovidData.classeAnalisi import Analisi
import numpy as np
from datetime import datetime, timedelta, date
from sklearn import linear_model
from sklearn.metrics import max_error
import prophet as Prophet
import json

datiCol = ["icu_patients", "icu_patients_per_million", "new_cases", "new_cases_per_million", "new_deaths", "new_deaths_per_million", "new_tests", "new_tests_per_thousand", "new_vaccinations", "people_fully_vaccinated", "people_fully_vaccinated_per_hundred", "people_vaccinated", "people_vaccinated_per_hundred", "positive_rate", "total_boosters", "total_boosters_per_hundred", "total_cases", "total_cases_per_million", "total_deaths", "total_deaths_per_million", "total_tests", "total_tests_per_thousand", "total_vaccinations", "total_vaccinations_per_hundred"]
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

dfTot = pd.read_csv("data/owid-dataset.csv",
                     parse_dates=["date"]
                     )



@app.callback(
    Output("fig-mondo", "figure"),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
)
def update_figMondo(input_dato, start_date, end_date):
    df = dfTot

    # Filter and clean df
    locationDel = ['World', 'Asia', 'Africa', 'Oceania', 'Europe', 'High income', 'Low income', 'Upper middle income',
                   'Lower middle income', 'North America', 'South America', 'European Union', 'Qatar']
    df = df[~df.location.isin(locationDel)]


    periodo = (df['date'] >= start_date) & (df['date'] <= end_date)
    df = df.loc[periodo]

    df['date'] = df['date'].dt.date.astype(str)

    # Columns renaming
    #df.columns = [col.lower() for col in df.columns]
    with open('data/custom.geo.json') as fp:
        data = json.load(fp)

    # Round off the locations to 2 decimal places (about 1.1 km accuracy)
    for i in range(0, len(data["features"])):
        for j in range(0, len(data["features"][i]['geometry']['coordinates'])):
            data["features"][i]['geometry']['coordinates'][j] = np.round(
                np.array(data["features"][i]['geometry']['coordinates'][j]), 2)


    px.set_mapbox_access_token(
        "pk.eyJ1IjoibWFuZnJlZG9mcmFjY29sYSIsImEiOiJja3hyd2JjbnEwNnVjMnBvNTZrbHBqdmwzIn0.YFYLdLUxoYC3gSpkcGplqQ")

    fig = px.choropleth_mapbox(df, geojson=data, locations='iso_code', color=input_dato,
                               featureidkey="properties.iso_a3",
                               #color_continuous_scale="Viridis",
                               color_continuous_scale=["rgb(55, 90, 127)", "rgb(0, 188, 140)"],
                               #range_color=(df[input_dato].min(), df[input_dato].max()),
                               # mapbox_style="carto-positron",
                               zoom=1, center={"lat": 24.8, "lon": 6.2},
                               opacity=0.5,
                               labels={input_dato: dictDati[input_dato]},
                               animation_frame='date',

                               )
    fig['layout']['updatemenus'][0]['pad'] = dict(r=10, t=10)
    fig['layout']['sliders'][0]['pad'] = dict(r=10, t=10, )
    # fig = px.choropleth(df, locations="iso_code",
    #                          color=input_dato,
    #                          hover_name="location",
    #                          animation_frame="date",
    #
    #                          #  title = "total_vaccinations_per_hundred",
    #                          color_continuous_scale=px.colors.sequential.Teal
    #
    #                          )

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 50

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

    # Filling nan values with 0
    #
    # # Compute bubble sizes
    # sizeInput = "size" + input_dato
    # df[sizeInput] = df[input_dato].apply(
    #     lambda x: (np.sqrt(x / 100) + 1) if x > 500 else (x / 2 + 1)).replace(
    #     np.NINF, 0)
    #
    # # Compute bubble color
    # colorInput = "color" + input_dato
    # df[colorInput] = (df["new_cases_per_million"] / df["new_deaths_per_million"]).fillna(0).replace(np.inf, 0)
    # df = df.fillna(0).replace(np.inf, 0)
    # df[sizeInput] = df[sizeInput].replace(np.inf, 0)
    #
    # days = df['date'].dt.date.unique().astype(str)
    #
    # df['date'] = df['date'].dt.date.astype(str)
    #
    # # days = ["2021-12-01", "2021-12-02"]
    # # print(tmp.head(10))
    # # colors = ["royalblue", "crimson", "lightseagreen", "orange", "lightgrey"]
    #
    # def generate_frame(day, input):
    #     sizeInput = "size" + input
    #     #colorInput = "color" + input
    #     # print(sizeInput, colorInput, day, df[df["date"] == day])
    #
    #     customDataList = []
    #     for i in datiCol:
    #         customDataList.append(df[df["date"] == day][i])
    #
    #     hoverTemplateList = []
    #     for i in datiCol:
    #         hoverTemplateList.append("%{customdata[" + i + "]}  <br>")
    #
    #     frame = {
    #         'name': 'frame_{}'.format(day),
    #         'data': {
    #             'type': 'scattermapbox',
    #             'lat': df[df["date"] == day]['latitude'],
    #             'lon': df[df["date"] == day]['longitude'],
    #             'marker': go.scattermapbox.Marker(
    #                 size=df[df["date"] == day][sizeInput],
    #                 color=df[df["date"] == day][colorInput],
    #                 # color=df[df["date"] == day][colorInput],
    #                 #    showscale=True,
    #                 #    colorbar={'title':'Recovered', 'titleside':'top', 'thickness':4, 'ticksuffix':' %'},
    #             ),
    #             'customdata': np.stack((df[df["date"] == day]['location'], df[df["date"] == day]['total_cases'],
    #                                     df[df["date"] == day]['new_cases'], df[df["date"] == day]['new_deaths']),
    #                                    axis=-1),
    #             'hovertemplate': "<extra></extra><em>%{customdata[0]}  </em><br>Total cases  %{customdata[1]}<br>New Cases  %{customdata[2]}<br>New deaths️  %{customdata[3]}",
    #         }
    #     }
    #     return frame
    #
    # frames = []
    # for day in days:
    #     frames.append(generate_frame(day, input_dato))
    #
    # # print(frames[0])
    #
    # sliders = [{
    #     'transition': {'duration': 0},
    #     'x': 0.08,
    #     'len': 0.88,
    #     'currentvalue': {'font': {'size': 15}, 'prefix': 'Date: ', 'visible': True, 'xanchor': 'center'},
    #     'steps': [
    #         {
    #             'label': day,
    #             'method': 'animate',
    #             'args': [
    #                 ['frame_{}'.format(day)],
    #                 {'mode': 'immediate', 'frame': {'duration': 100, 'redraw': True}, 'transition': {'duration': 50}}
    #             ],
    #         } for day in days]
    # }]
    #
    # # Defining the initial state
    # data = frames[0]['data']
    #
    # play_button = [{
    #     'type': 'buttons',
    #     'showactive': True,
    #     'x': 0.045, 'y': -0.08,
    #     'buttons': [{
    #         'label': '▶',  # Play
    #         'method': 'animate',
    #         'args': [
    #             None,
    #             {
    #                 'frame': {'duration': 100, 'redraw': True},
    #                 'transition': {'duration': 50},
    #                 'fromcurrent': True,
    #                 'mode': 'immediate',
    #             }
    #         ]
    #     }]
    # }]
    #
    # # Adding all sliders and play button to the layout
    # layout = go.Layout(
    #     sliders=sliders,
    #     paper_bgcolor='rgba(0,0,0,0)',
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     font_color='#fff',
    #     updatemenus=[{
    #         'type': 'buttons',
    #         'showactive': True,
    #         'x': 0.045, 'y': -0.08,
    #         'bgcolor': 'rgba(255,255,255,1)',
    #         'font': {
    #             'color': '#000',
    #         },
    #         'buttons': [{
    #             'label': '▶',  # Play
    #             'method': 'animate',
    #             'args': [
    #                 None,
    #                 {
    #                     'frame': {'duration': 100, 'redraw': True},
    #                     'transition': {'duration': 50},
    #                     'fromcurrent': True,
    #                     'mode': 'immediate',
    #                 }
    #             ]
    #         }]
    #     }],
    #     mapbox={
    #         'accesstoken': "pk.eyJ1IjoibWFuZnJlZG9mcmFjY29sYSIsImEiOiJja3hyd2JjbnEwNnVjMnBvNTZrbHBqdmwzIn0.YFYLdLUxoYC3gSpkcGplqQ",
    #         'center': {"lat": 37.86, "lon": 2.15},
    #         'zoom': 1.7,
    #         'style': 'light',
    #     },
    #     legend=dict(
    #         yanchor="top",
    #         y=0.97,
    #         xanchor="left",
    #         x=0.01),
    #     margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
    #     # showlegend = True
    # )
    #
    # # Creating the figure
    # fig = go.Figure(data=data, layout=layout, frames=frames)

    return fig


# UPDATE TITOLO MONDO
@app.callback(
    Output("titolo-mondo", "children"),
    Input("dato-input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
)
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


# CONFRONTO NUMERICO NAZIONE 1
@app.callback(
    Output("dati-nazione-1", "children"),
    Input('input-nazione-1', 'value'),
    Input("dato-input-1", "value"),
    Input('date-confronto', 'start_date'),
    Input('date-confronto', 'end_date'),
)
def updateNazione(nazione, dato, start_date, end_date):
    df = Analisi(nazione, dfTot).df
    # df['date'] = pd.to_datetime(df['date'])
    periodo = (df["date"] > start_date) & (df["date"] <= end_date)
    datiCol = [dato]
    # mldt.append(i)
    df = df[datiCol]
    df = df.loc[periodo]
    titDato = dictDati[dato] + " - " + nazione
    outputNazione = dbc.ListGroup(
        [
            dbc.ListGroupItem(titDato,
                              color="primary",
                              className="bg-info"
                              ),
            dbc.ListGroupItem(["Media", dbc.Badge(round(df[dato].mean(), 2), color="light", text_color="primary", className="ms-1"),],color="primary"),
            dbc.ListGroupItem(["Minimo", dbc.Badge(df[dato].min(), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),
            dbc.ListGroupItem(["Massimo", dbc.Badge(df[dato].max(), color="light", text_color="primary",
                                                  className="ms-1"), ], color="primary"),

        ]
    )
    return outputNazione


# update country 2 on input
@app.callback(
    Output("dati-nazione-2", "children"),
    Input('input-nazione-2', 'value'),
    Input("dato-input-2", "value"),
    Input('date-confronto', 'start_date'),
    Input('date-confronto', 'end_date'),
)
def updateNazione(nazione, dato, start_date, end_date):
    df = Analisi(nazione, dfTot).df
    # df['date'] = pd.to_datetime(df['date'])
    periodo = (df["date"] > start_date) & (df["date"] <= end_date)
    datiCol = [dato]
    # mldt.append(i)
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


# FIGURA CONFRONTO
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
    def generateDf(nazione, dato):
        df = Analisi(nazione, dfTot).df
        # df['date'] = pd.to_datetime(df['date'])
        periodo = (df["date"] > start_date) & (df["date"] <= end_date)
        datiCol = ["date", dato]
        # mldt.append(i)
        df = df[datiCol]
        df = df.loc[periodo]
        return df

    df1 = generateDf(nazione1, datoInputOne)
    df2 = generateDf(nazione2, datoInputTwo)

    # Creating the figure
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


#UPDATE TITOLO MACHINE LEARNING

@app.callback(
    Output("titolo-ML", "children"),
    Input("dato-input-ML", "value"),
    Input("input-nazione-ML", "value"),
)
def updateTitML(dato, nazione):
    df = Analisi(nazione, dfTot).df
    #print("DF head nazione ML")
    #print(df.head(10))
    inizio = df["date"].iloc[0].strftime("%d/%m/%Y")
    fine = df["date"].iloc[-1].strftime("%d/%m/%Y")
    periodo = "Trend: " + inizio + " - " + fine + " | Proiezione: 100 giorni"
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
    return x

# update fig ML
@app.callback(
    Output("fig-ML", "figure"),
    Input('dato-input-ML', 'value'),
    Input('input-nazione-ML', 'value'),
)
def updateFigML(dato_input, nazione):
    from datetime import date as dt
    data = dfTot
    data = data[data["location"] == nazione]
    #print(data.columns)
    import numpy as np
    data = data.fillna(0).replace(np.inf, 0)

    # data['diff_tamponi'] = data['tamponi'].diff()
    dates = data['date']
    date_format = [pd.to_datetime(d) for d in dates]

    import numpy as np

    # prepare the lists for the model
    X = date_format
    y = data[dato_input].tolist()[1:]

    # date format is not suitable for modeling, let's transform the date into incrementals number starting from April 1st
    starting_date = 1  # April 1st is the 37th day of the series
    day_numbers = []
    for i in range(1, len(X)):
        day_numbers.append([i])
    X = day_numbers
    # # let's train our model only with data after the peak
    X = X[starting_date:]
    y = y[starting_date:]
    # Instantiate Linear Regression
    linear_regr = linear_model.LinearRegression()

    # Train the model using the training sets
    linear_regr.fit(X, y)
    #print("Linear Regression Model Score: %s" % (linear_regr.score(X, y)))
    # Predict future trend
    import numpy as np
    import math
    y_pred = linear_regr.predict(X)
    #print(y_pred)
    error = max_error(y, y_pred)
    X_test = []
    future_days = 1000
    for i in range(starting_date, starting_date + future_days):
        X_test.append([i])
    #print(X_test)
    y_pred_linear = linear_regr.predict(X_test)

    # for i in range(starting_date, starting_date + future_days):
    #   X_test.append([i])
    y_pred_linear = linear_regr.predict(X_test)

    y_pred_max = []
    y_pred_min = []
    for i in range(0, len(y_pred_linear)):
        y_pred_max.append(y_pred_linear[i] + error)
        y_pred_min.append(y_pred_linear[i] - error)

    #print(y_pred_max)
    #print(y_pred_min)
    #print(y_pred_linear)
    #print(X_test)

    new_df = pd.DataFrame(list(zip(X_test, y_pred_max, y_pred_min, y_pred_linear)),
                          columns=['indice', 'massimo', "minimo", "predictions"])

    nuovo_indice = []
    date_indicizzate = []

    # date_time_str = data["date"].iloc[-1]
    date_time_str = "2020-04-01"

    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d') + timedelta(days=1)

    # print(date_time_obj)

    for i in range(0, len(new_df.indice)):
        nuovo_indice.append(new_df.indice[i][0])
        date_indicizzate.append(date_time_obj + timedelta(days=i)

                                )

    new_df["indice"] = date_indicizzate

    #print(new_df.tail())
    #print(new_df.dtypes)

    tmp = data
    keep = ["date", dato_input]
    tmp = tmp[keep]
    #print(tmp.head(10))

    tmp.columns = ['ds', 'y']
    tmp['ds'] = pd.to_datetime(tmp['ds']).dt.date
    # print(dfML.tail())
    m = Prophet.Prophet(weekly_seasonality=True)
    m.fit(tmp)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    #print(forecast.tail(10))

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


    # fig.update_yaxes(type="log")
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
    # fig.update_xaxes(range=[start_date, end_date])

    # fig.show()
    return fig
