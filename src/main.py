import pandas as pd
from datetime import datetime

# Carrega os dados
dados = pd.read_csv('dados.csv')

# Calcula a distância percorrida
dados['Distancia'] = dados['Km final'] - dados['Km inicial']

# Converte a coluna 'Data' para datetime
dados['Data'] = pd.to_datetime(dados['Data'], dayfirst=True)

def filtrar_por_mes_ano(dataframe, mes, ano):
    """Filtra o DataFrame por um determinado mês e ano."""
    inicio_mes = pd.to_datetime(f'01/{mes}/{ano}', dayfirst=True)
    fim_mes = inicio_mes + pd.offsets.MonthEnd(0)  # Fim do mês corrente
    mascara = (dataframe['Data'] >= inicio_mes) & (dataframe['Data'] <= fim_mes)
    return dataframe[mascara]

def gerar_resumo(dataframe_filtrado):
    """Gera um resumo da distância percorrida e consumo de diesel por motorista."""
    if dataframe_filtrado.empty:
        print("Nenhum dado encontrado para o período.")
        return

    resumo_motoristas = dataframe_filtrado.groupby('Nome do motorista').agg(
        Distancia=('Distancia', 'sum'),
        Total_Diesel=('Óleo diesel', 'sum')
    ).reset_index()

    resumo_motoristas['KM_por_L'] = round(resumo_motoristas['Distancia'] / resumo_motoristas['Total_Diesel'], 2)
    print(resumo_motoristas)

def distancia_errada(dataframe_filtrado):
    # Verificar linhas com distância <= 0 ou > 700
        anomalous_distances = dataframe_filtrado[(dataframe_filtrado['Distancia'] <= 0) | (dataframe_filtrado['Distancia'] > 700)]

        if anomalous_distances.empty:
            print(f"Nenhuma linha com distância anômala foi encontrada em {mes}/{ano}.")
        else:
            print(f"Linhas com distância anômala em {mes}/{ano}:")
            print(anomalous_distances[['Data', 'Placa', 'Nome do motorista', 'Distancia']])



def datas_duplicadas(dataframe_filtrado):
     # Verificar motoristas com datas duplicadas
        duplicated_entries = dataframe_filtrado[dataframe_filtrado.duplicated(subset=['Nome do motorista', 'Data'], keep=False)]

        if duplicated_entries.empty:
            print(f"Nenhum motorista com datas duplicadas foi encontrado em {mes}/{ano}.")
        else:
            print(f"Motoristas com datas duplicadas em {mes}/{ano}:")
            print(duplicated_entries[['Nome do motorista', 'Data']])
     



# Define o mês e ano desejados
mes = input("Digite o número referente ao mẽs: ")
ano = input("Digite o número referente ao ano: ")

# Filtra os dados
dados_filtrados = filtrar_por_mes_ano(dados, mes, ano)

# Gera o resumo
gerar_resumo(dados_filtrados)
distancia_errada(dados_filtrados)
datas_duplicadas(dados_filtrados)