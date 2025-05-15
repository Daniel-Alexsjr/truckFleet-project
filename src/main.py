import pandas as pd

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

# Define o mês e ano desejados
mes = 4
ano = 2025

# Filtra os dados
dados_filtrados = filtrar_por_mes_ano(dados, mes, ano)

# Gera o resumo
gerar_resumo(dados_filtrados)