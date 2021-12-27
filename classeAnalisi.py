import pandas as pd
import plotly.graph_objects as go
import plotly.express as ex
from datetime import timedelta, date # pacchetto datetime per utilizzo e manipolaizione date

class Analisi:
    def __init__(self, paese):
        self.df = pd.read_csv("data/owid-dataset.csv")

        self.df = self.df[self.df["location"] == paese]

        self.fig = go.Figure(
            go.Bar(hoverinfo='skip',
                    x=self.df["date"],
                    y=self.df["new_deaths"]
                   )
            )

        self.figTot = go.Figure()
        self.figTot.add_trace(
            go.Scatter(x=self.df.date, y=self.df.columns, name='Deceduti', fill='tonexty', connectgaps=True))
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
