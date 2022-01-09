#definisco classe analisi per filtro dataset in base alla nazione 
class Analisi:
    def __init__(self, paese , df):
#filtra il dataframe mantenendo le righe in cui il valore della colonna location è uguale a paese  
        self.df = df[df["location"] == paese]
