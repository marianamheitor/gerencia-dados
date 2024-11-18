import pandas as pd
import json

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
        df[coluna] = pd.to_numeric(df[coluna].str.replace(',', '.'), errors='coerce').fillna(0)
    
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

# Função para salvar os dados em JSON
def salvar_como_json(nome_cidade, dados, metadados, caminho_json):
    json_data = []
    for _, row in dados.iterrows():
        entrada = {
            "Data": row["Data"].strftime('%Y-%m-%d'),
            "Metadados": metadados,
            "Dados": row.to_dict()
        }
        entrada["Dados"].pop("Data", None)  # Remover redundância de data no nível dos dados
        json_data.append(entrada)
    
    # Salvar em arquivo JSON
    with open(caminho_json, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)
    print(f"JSON gerado para {nome_cidade}: {caminho_json}")

# Processar os dados de cada cidade
arquivos_cidades = {
    "Farroupilha": "data/INMET_S_RS_A840_BENTO GONCALVES_01-01-2023_A_31-12-2023.CSV",
    "Lages": "data/INMET_S_SC_A865_LAGES_01-01-2023_A_31-12-2023.CSV",
    "São Mateus do Sul": "data/INMET_S_PR_A874_SAO MATEUS DO SUL_01-01-2023_A_31-12-2023.CSV"
}

# Iterar sobre os arquivos e processar
for cidade, caminho in arquivos_cidades.items():
    metadados, estatisticas_diarias = processar_arquivo_meteorologico(caminho)
    caminho_json = f"{cidade.replace(' ', '_').lower()}_dados.json"
    salvar_como_json(cidade, estatisticas_diarias, metadados, caminho_json)
