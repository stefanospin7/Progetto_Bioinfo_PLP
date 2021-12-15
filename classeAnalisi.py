import pandas as pd
import plotly.graph_objects as go
import plotly.express as ex
class Analisi:
    def __init__(self, csv):
        self.df = pd.read_csv(csv)

        self.fig = go.Figure(
            go.Bar(hoverinfo='skip',
                    x=self.df["data"],
                    y=self.df["deceduti"]
                   )
            )

"""italia = Analisi("data/datiCovidItalia.csv")
italia.fig.show() 
cina = Analisi("data/datiCovidCina.csv")
cina.fig.show() """
