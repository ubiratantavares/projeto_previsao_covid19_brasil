from database import Database
from analise import Exploratoria, SerieTemporal
import pandas as pd

# ler o database
database = Database(url='https://github.com/neylsoncrepalde/projeto_eda_covid/blob/master/covid_19_data.csv?raw=true',
                    column1='ObservationDate',
                    column2='Last Update')

# cria o dataframe
df = database.df

# lista os 5 primeiros registros da base de dados
print(df.head())

# verifica os nomes e os tipos dos atributos da base de dados
database.verificarTiposColunas()

analisa = Exploratoria()

brasil = analisa.verificarNumeroCasosConfirmados(df)

# analise exploratoria dos dados
analisa.graficoNumeroCasosConfirmados(brasil)
analisa.graficoNumeroNovosCasosConfirmadosPorDia(brasil)
analisa.graficoNumeroCasosConfirmados(brasil)
analisa.verificarTaxaCrescimento(brasil)
analisa.verificarTaxaCrescimentoPorDia(brasil)

# analise temporal
st = SerieTemporal()

# analise grafica da serie temporal para os novos casos
novoscasos = brasil.novoscasos
novoscasos.index = brasil.observationdate
st.analiseGrafica(novoscasos)

# analise grafica da serie temporal para os casos confirmados
confirmados = brasil.confirmed
confirmados.index = brasil.observationdate
st.analiseGrafica(confirmados)

# previsão de casos com o modelo arima
modelo = st.modeloArima(confirmados)
st.analiseGraficaPrevisao(confirmados, modelo, pd.date_range('2020-05-20', '2020-06-05'))
