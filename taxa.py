import pandas as pd
import numpy as np


class Taxa:

    def taxa_crescimento(self, data, variable, data_inicio=None, data_fim=None):
        # Se data_inicio for None, define como a primeira data disponível no dataset
        if data_inicio == None:
            data_inicio = data.observationdate.loc[data[variable] > 0].min()
        else:
            data_inicio = pd.to_datetime(data_inicio)

        if data_fim == None:
            data_fim = data.observationdate.iloc[-1]
        else:
            data_fim = pd.to_datetime(data_fim)

        # Define os valores de presente e passado
        passado = data.loc[data.observationdate == data_inicio, variable].values[0]
        presente = data.loc[data.observationdate == data_fim, variable].values[0]

        # Define o número de pontos no tempo q vamos avaliar
        n = (data_fim - data_inicio).days

        # Calcula a taxa
        taxa = (presente / passado) ** (1 / n) - 1

        return taxa * 100


    def taxa_crescimento_diaria(self, data, variable, data_inicio=None):
        if data_inicio == None:
            data_inicio = data.observationdate.loc[data[variable] > 0].min()
        else:
            data_inicio = pd.to_datetime(data_inicio)

        data_fim = data.observationdate.max()
        n = (data_fim - data_inicio).days
        taxas = list(map(
            lambda x: (data[variable].iloc[x] - data[variable].iloc[x - 1]) / data[variable].iloc[x - 1],
            range(1, n + 1)
        ))
        return np.array(taxas) * 100