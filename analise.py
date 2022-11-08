import numpy as np

import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go

from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima.arima import auto_arima

from taxa import Taxa

class Exploratoria:

    # verifica o numero de casos confirmados
    def verificarNumeroCasosConfirmados(self, df):
        brasil = df.loc[(df.countryregion == 'Brazil') & (df.confirmed > 0)]
        confirmados = brasil['confirmed']
        # verifica o numero de novos casos por dia - inserção de novo recurso
        brasil['novoscasos'] = list(map(lambda x: 0 if x == 0 else confirmados.iloc[x] - confirmados.iloc[x - 1],
                                    np.arange(brasil.shape[0])))
        return brasil


    # verifica a taxa de crescimento
    def verificarTaxaCrescimento(self, data):
        tx = Taxa()
        cresc_medio = tx.taxa_crescimento(data, 'confirmed')
        print(f"O crescimento médio do COVID no Brasil no período avaliado foi de {cresc_medio.round(2)}%.")
        return None


    # verifica a taxa de crescimento por dia
    def verificarTaxaCrescimentoPorDia(self, data):
        tx = Taxa()
        tx_dia = tx.taxa_crescimento_diaria(data, 'confirmed')
        print(tx_dia)
        return None


    def graficoNumeroCasosConfirmados(self, data):
        fig = px.line(data,
                      x='observationdate',
                      y='confirmed',
                      labels={'observationdate': 'Data', 'confirmed': 'Número de casos confirmados'},
                      title='Casos confirmados no Brasil')
        fig.show()
        return None


    def graficoNumeroNovosCasosConfirmadosPorDia(self, data):
        fig = px.line(data,
                      x='observationdate',
                      y='novoscasos',
                      labels={'observationdate': 'Data', 'novoscasos': 'Novos casos'},
                      title='Novos casos por dia')
        fig.show()
        return None

    # verifica o numero de casos de mortes
    def graficoNumeroCasosMortes(self, data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.observationdate,
                                 y=data.deaths,
                                 name='Mortes',
                                 mode='lines+markers',
                                 line=dict(color='red')))
        fig.update_layout(title='Mortes por COVID-19 no Brasil',
                          xaxis_title='Data',
                          yaxis_title='Número de mortes')
        fig.show()
        return None

class SerieTemporal:

    def analiseGrafica(self, data):
        res = seasonal_decompose(data)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))
        ax1.plot(res.observed)
        ax2.plot(res.trend)
        ax3.plot(res.seasonal)
        ax4.scatter(data.index, res.resid)
        ax4.axhline(0, linestyle='dashed', c='black')
        plt.show()

    def modeloArima(self, data):
        modelo = auto_arima(data)
        return modelo


    def analiseGraficaPrevisao(self, data, model, datas):
        fig = go.Figure(go.Scatter(x=data.index, y=data, name='Observed'))
        fig.add_trace(go.Scatter(x=data.index, y=model.predict_in_sample(), name='Predicted'))
        numero_de_dias = len(list(datas))
        fig.add_trace(go.Scatter(x=datas, y=model.predict(numero_de_dias), name='Forecast'))
        fig.update_layout(title='Previsão de casos confirmados para os próximos {} dias'.format(numero_de_dias),
                          yaxis_title='Casos confirmados', xaxis_title='Data')
        fig.show()