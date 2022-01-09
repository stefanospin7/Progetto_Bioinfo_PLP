import pandas as pd
import plotly.graph_objects as go
import plotly.express as ex
from datetime import timedelta, date # pacchetto datetime per utilizzo e manipolaizione date


class Analisi:

    def __init__(self, paese , df):


        self.df = df[df["location"] == paese]

