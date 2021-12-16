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



"""italia = Analisi("data/datiCovidItalia.csv")
italia.fig.show() 
cina = Analisi("data/datiCovidCina.csv")
cina.fig.show() """
