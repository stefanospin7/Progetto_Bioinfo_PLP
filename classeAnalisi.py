import pandas as pd
import plotly.graph_objects as go
import plotly.express as ex
from datetime import timedelta, date # pacchetto datetime per utilizzo e manipolaizione date

class Analisi:
    def __init__(self, csv):
        self.df = pd.read_csv(csv)

        self.fig = go.Figure(
            go.Bar(hoverinfo='skip',
                    x=self.df["data"],
                    y=self.df["deceduti"]
                   )
            )

        self.figTot = go.Figure()
        self.figTot.add_trace(
            go.Scatter(x=self.df.data, y=self.df.deceduti, name='Deceduti', fill='tonexty', connectgaps=True))
        self.figTot.add_trace(
            go.Scatter(x=self.df.data, y=self.df.totale_positivi, name='Totale Positivi', fill='tonexty', connectgaps=True))
        self.figTot.add_trace(
            go.Scatter(x=self.df.data, y=self.df.nuovi_positivi, name='Nuovi Positivi', fill='tonexty', connectgaps=True))
        self.figTot.add_trace(
            go.Scatter(x=self.df.data, y=self.df.terapia_intensiva, name='Terapia Intensiva', fill='tonexty', connectgaps=True))
        self.figTot.add_trace(
            go.Scatter(x=self.df.data, y=self.df.totale_ospedalizzati, name='Totale Ospedalizzati', fill='tonexty', connectgaps=True))
        self.figTot.add_trace(
            go.Scatter(x=self.df.data, y=self.df.tamponi, name='Tamponi', fill='tonexty', connectgaps=True))
        self.figTot.update_yaxes(type="log")
        self.figTot.update_layout(
            legend=dict(
                yanchor="top",
                y=0.97,
                xanchor="left",
                x=0.01),
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            showlegend=True
        )

        start_date = date(2020, 2, 24)
        end_date = date.today()
        self.figTot.update_xaxes(range=[start_date, end_date])



"""italia = Analisi("data/datiCovidItalia.csv")
italia.fig.show() 
cina = Analisi("data/datiCovidCina.csv")
cina.fig.show() """
