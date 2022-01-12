# defying "Analisi" class to filter dataset according to the specific Nation 
class Analisi:
    def __init__(self, paese , df):
# filtering dataframe keeping only the rows in which the data of the column location correspond (equal) to  "paese"  
        self.df = df[df["location"] == paese]
