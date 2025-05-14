print("hello world, estou usando docker")

import pandas as pd

data = pd.read_csv('dados.csv')
print(data.head())
print(data.columns)

# Solicitar ao usuário o mês e ano
month = 4 #input("Digite o mês (mm): ")
year = 2025 #input("Digite o ano (yyyy): ")


# Calcular a distância percorrida
data['Distancia'] = data['Km final'] - data['Km inicial']
pd.set_option("display.max_columns", 20)  # mostra até 20 colunas
pd.set_option("display.width", 200) 
# Converter a coluna 'Data' para o formato datetime especificando que o dia vem primeiro
data['Data'] = pd.to_datetime(data['Data'], dayfirst=True)

def filter_data(month, year):
    try:
        # Criar datas de início e fim do mês usando o primeiro e último dia do mês fornecido
        start_date = pd.to_datetime(f'01/{month}/{year}', dayfirst=True)
        end_date = start_date + pd.offsets.MonthEnd(1)

        # Filtrar os dados
        mask = (data['Data'] >= start_date) & (data['Data'] <= end_date)
        filtered_data = data[mask]

        if filtered_data.empty:
            print("Nenhum dado encontrado para o período selecionado.")
        else:
            # Agrupar os dados filtrados por 'Nome do motorista', somar as distâncias e o óleo diesel
            distancias_motorista = filtered_data.groupby('Nome do motorista').agg({
                'Distancia': 'sum',
                'Óleo diesel': 'sum'
            }).reset_index()

            # Renomear a coluna para clareza
            distancias_motorista = distancias_motorista.rename(columns={'Óleo diesel': 'Total Diesel'})

            # Adicionar a coluna 'KM por L' dividindo a Distancia pelo Total Diesel
            distancias_motorista['KM por L'] = round(distancias_motorista['Distancia'] / distancias_motorista['Total Diesel'], 2)

            print(distancias_motorista)
    except Exception as e:
        print("Erro:", str(e))

# Exemplo de uso
filter_data(month, year)  # Insira o mês e ano desejados
