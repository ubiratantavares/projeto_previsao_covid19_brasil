import pandas as pd
import re

class Database:

    def __init__(self, url, column1, column2):
        self.__url = url
        self.__column1 = column1
        self.__column2 = column2
        self.__df = self.__ler()

    def __ler(self):
        df = pd.read_csv(self.__url, parse_dates=[self.__column1, self.__column2])
        # corrige o nome das colunas
        df.columns = [re.sub(r"[/| ]", "", col).lower() for col in df.columns]
        return df

    @property
    def df(self):
        return self.__df

    def verificarTiposColunas(self):
        print(self.df.dtypes)
