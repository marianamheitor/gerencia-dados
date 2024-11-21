import os
import requests
import zipfile
import pandas as pd
import json
from datetime import datetime

# Diretórios para armazenar arquivos
diretorio_zip = "dados_zip"
diretorio_dados = "dados_descompactados"
os.makedirs(diretorio_zip, exist_ok=True)
os.makedirs(diretorio_dados, exist_ok=True)

# URLs dos arquivos a serem baixados
urls = {
    "2023": "https://portal.inmet.gov.br/uploads/dadoshistoricos/2023.zip",
    "2024": "https://portal.inmet.gov.br/uploads/dadoshistoricos/2024.zip"
}

# Cidades de interesse e códigos associados
cidades_cods = {
    "Farroupilha": "A840",
    "Lages": "A865",
    "São Mateus do Sul": "A874"
}

# Período de interesse
inicio_periodo = datetime(2023, 10, 1)
fim_periodo = datetime(2024, 10, 31)

# Função para baixar arquivos ZIP
def baixar_arquivos():
    for ano, url in urls.items():
        caminho_zip = os.path.join(diretorio_zip, f"{ano}.zip")
        if os.path.exists(caminho_zip):
            print(f"Arquivo de {ano} já baixado. Pulando download.")
            continue

        print(f"Baixando dados de {ano}...")
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, stream=True)

            if response.status_code == 200:
                with open(caminho_zip, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"Dados de {ano} baixados com sucesso!")
            else:
                print(f"Erro ao baixar dados de {ano}: {response.status_code} - {response.reason}")
                continue

            if not zipfile.is_zipfile(caminho_zip):
                print(f"Erro: O arquivo {caminho_zip} não é um ZIP válido. Removendo arquivo...")
                os.remove(caminho_zip)
            else:
                with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
                    zip_ref.extractall(diretorio_dados)
                print(f"Dados de {ano} descompactados com sucesso!")
        except Exception as e:
            print(f"Erro ao baixar ou descompactar os dados de {ano}: {e}")

# Função ajustada para renomear colunas, corrigir formato e garantir inclusão de dados de 2023.
def processar_arquivo_meteorologico(caminho_arquivo):
    try:
        print(f"Processando o arquivo: {caminho_arquivo}")
        with open(caminho_arquivo, 'r', encoding='latin1') as file:
            linhas = file.readlines()

        if len(linhas) < 10:
            print(f"O arquivo {caminho_arquivo} parece estar vazio ou incompleto.")
            return {}, pd.DataFrame()

        metadados = {}
        i = 0
        while not linhas[i].startswith("Data;Hora UTC"):
            chave, valor = linhas[i].strip().split(';')
            metadados[chave.strip()] = valor.strip()
            i += 1

        cabecalhos = linhas[i].strip().split(';')
        dados = [linha.strip().split(';') for linha in linhas[i + 1:] if linha.strip()]
        df = pd.DataFrame(dados, columns=cabecalhos)
        df.columns = df.columns.str.strip()

        # Conversão e limpeza de dados
        df['Data'] = pd.to_datetime(df['Data'], format='%Y/%m/%d', errors='coerce')
        for col in df.columns:
            if col not in ['Data', 'Hora UTC']:
                df[col] = pd.to_numeric(df[col].str.replace(',', '.'), errors='coerce')

        # Filtrar pelo período
        df = df[(df['Data'] >= inicio_periodo) & (df['Data'] <= fim_periodo)]

        if df.empty:
            print(f"Arquivo {caminho_arquivo} não contém dados no período solicitado.")
            return {}, pd.DataFrame()

        # Renomear e padronizar colunas
        df.rename(columns={
            'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': 'Pressao (mean)',
            'RADIACAO GLOBAL (Kj/m²)': 'Radiacao Global (mean)',
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'Temp Bulbo Seco (mean)',
            'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)': 'Temp Max (max)',
            'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)': 'Temp Min (min)',
            'UMIDADE RELATIVA DO AR, HORARIA (%)': 'Umidade Relativa (mean)',
            'VENTO, VELOCIDADE HORARIA (m/s)': 'Velocidade Vento (mean)'
        }, inplace=True)

        # Agregar estatísticas diárias
        estatisticas_diarias = df.groupby('Data').agg({
            'Pressao (mean)': ['mean', 'max', 'min'],
            'Radiacao Global (mean)': 'mean',
            'Temp Bulbo Seco (mean)': 'mean',
            'Temp Max (max)': 'max',
            'Temp Min (min)': 'min',
            'Umidade Relativa (mean)': 'mean',
            'Velocidade Vento (mean)': 'mean'
        }).reset_index()

        estatisticas_diarias.columns = ['Data'] + [
            f'{col[0]} ({col[1]})' if col[1] else col[0] for col in estatisticas_diarias.columns[1:]
        ]

        print(f"Arquivo processado com sucesso: {caminho_arquivo}")
        return metadados, estatisticas_diarias
    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {e}")
        return {}, pd.DataFrame()


# Função para salvar os dados em JSON
def salvar_como_json(nome_cidade, dados, metadados, caminho_json):
    json_data = {
        "Metadados": metadados,
        "Dados": []
    }
    for _, row in dados.iterrows():
        entrada = {key: row[key] for key in row.index if key != "Data"}
        entrada["Data"] = row["Data"].strftime('%Y-%m-%d')
        json_data["Dados"].append(entrada)

    with open(caminho_json, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)
    print(f"JSON gerado para {nome_cidade}: {caminho_json}")


# Script principal ajustado
if __name__ == "__main__":
    baixar_arquivos()
    for cidade, codigo in cidades_cods.items():
        arquivos = [f for f in os.listdir(diretorio_dados) if codigo in f]
        if not arquivos:
            print(f"Nenhum arquivo encontrado para {cidade}")
            continue

        for arquivo in arquivos:
            caminho_arquivo = os.path.join(diretorio_dados, arquivo)
            metadados, estatisticas_diarias = processar_arquivo_meteorologico(caminho_arquivo)
            
            if not estatisticas_diarias.empty:
                # Filtrar os dados por ano
                for ano in ["2023", "2024"]:
                    dados_ano = estatisticas_diarias[
                        estatisticas_diarias['Data'].dt.year == int(ano)
                    ]
                    if not dados_ano.empty:
                        caminho_json = f"{cidade.replace(' ', '_').lower()}_dados_{ano}.json"
                        salvar_como_json(cidade, dados_ano, metadados, caminho_json)
