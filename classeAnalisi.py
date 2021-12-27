import pandas as pd
import plotly.graph_objects as go
import plotly.express as ex
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



"""italia = Analisi("data/datiCovidItalia.csv")
italia.fig.show() 
cina = Analisi("data/datiCovidCina.csv")
cina.fig.show() """
