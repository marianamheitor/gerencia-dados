import pandas as pd

# Função para processar o arquivo meteorológico
def processar_arquivo_meteorologico(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='latin1') as file:
        linhas = file.readlines()
    
    # Separar metadados
    metadados = {}
    i = 0
    while not linhas[i].startswith("Data;Hora UTC"):
        chave, valor = linhas[i].strip().split(';')
        metadados[chave.strip()] = valor.strip()
        i += 1
    
    # Ler os dados a partir da linha dos cabeçalhos
    cabecalhos = linhas[i].strip().split(';')
    dados = [linha.strip().split(';') for linha in linhas[i + 1:] if linha.strip()]
    
    # Criar DataFrame e ajustar colunas
    df = pd.DataFrame(dados, columns=cabecalhos)
    df.columns = df.columns.str.strip()
    
    # Converter colunas numéricas
    for coluna in df.columns[2:]:
        df[coluna] = pd.to_numeric(df[coluna].str.replace(',', '.'), errors='coerce')
    
    # Agrupamento por dia
    df['Data'] = pd.to_datetime(df['Data'], format='%Y/%m/%d')
    estatisticas_diarias = df.groupby('Data').agg({
        'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': ['mean', 'max', 'min'],
        'RADIACAO GLOBAL (Kj/m²)': 'mean',
        'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'mean',
        'TEMPERATURA DO PONTO DE ORVALHO (°C)': 'mean',
        'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)': 'max',
        'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)': 'min',
        'UMIDADE RELATIVA DO AR, HORARIA (%)': 'mean',
        'UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)': 'max',
        'UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)': 'min',
        'VENTO, DIREÇÃO HORARIA (gr) (° (gr))': 'mean',
        'VENTO, RAJADA MAXIMA (m/s)': 'max',
        'VENTO, VELOCIDADE HORARIA (m/s)': 'mean'
    }).reset_index()
    
    # Renomear colunas para clareza
    estatisticas_diarias.columns = ['Data'] + [
        f'{col[0]} ({col[1]})' if col[1] else col[0] for col in estatisticas_diarias.columns[1:]
    ]
    
    return metadados, estatisticas_diarias

# Caminho do arquivo de exemplo
caminho = 'data/INMET_S_PR_A874_SAO MATEUS DO SUL_01-01-2023_A_31-12-2023.CSV'
metadados, estatisticas_diarias = processar_arquivo_meteorologico(caminho)

# Exibir dados dos dois primeiros dias no formato solicitado
for i in range(2):  # Exibir apenas os dois primeiros dias
    dia = estatisticas_diarias.iloc[i, 0].strftime('%d-%m-%Y')
    print(f"dia:{dia}")
    print("dados")
    print(estatisticas_diarias.iloc[i, 1:])
    print()
