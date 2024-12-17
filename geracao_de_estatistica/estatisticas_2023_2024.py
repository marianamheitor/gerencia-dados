import json
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar o arquivo JSON
def carregar_json(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        dados_json = json.load(file)
    return dados_json

# Função para extrair dados dos arquivos JSON e converter em DataFrame
def extrair_dados_json(dados_json):
    dados = dados_json['Dados']
    df = pd.DataFrame(dados)
    df['Data'] = pd.to_datetime(df['Data'])  # Converter a coluna 'Data' para datetime
    return df

# Função para calcular estatísticas importantes
def analise_estatisticas(df):
    # Calcular médias e outros valores estatísticos relevantes
    estatisticas = df.describe()
    return estatisticas

# Função para analisar condições climáticas
def analisar_condicoes_colheita(df):
    # Verificar a média de temperatura, precipitação, vento, pressão e umidade
    media_temp_max = df['Temp Max (max) (max)'].mean()
    media_temp_min = df['Temp Min (min) (min)'].mean()
    total_precipitacao = df['Precipitacao Total (soma) (sum)'].sum()
    media_vento = df['Velocidade Vento (mean) (mean)'].mean()
    media_pressao = df['Pressao (mean) (mean)'].mean()
    media_umidade = df['Umidade Relativa (mean) (mean)'].mean()

    return media_temp_max, media_temp_min, total_precipitacao, media_vento, media_pressao, media_umidade

# Função para inferir impacto climático na produção de kiwi
def inferir_impacto_na_producao(media_temp_max, media_temp_min, total_precipitacao, media_vento, media_pressao, media_umidade):
    if media_temp_max > 30 or media_temp_min < -5:
        return "Condições climáticas desfavoráveis para a produção de kiwi."
    elif total_precipitacao > 100:
        return "Excesso de precipitação, pode afetar negativamente a produção."
    elif media_vento > 5:
        return "Ventos fortes, pode prejudicar a produção de kiwi."
    elif media_pressao < 920 or media_pressao > 1030:
        return "Pressão atmosférica fora do normal, pode impactar a produção."
    elif media_umidade > 90:
        return "Umidade muito alta, pode favorecer o desenvolvimento de doenças nas plantas."
    else:
        return "Condições climáticas favoráveis para a produção de kiwi."

# Função para plotar gráficos de temperatura, precipitação e umidade
def plotar_graficos(df, cidade_nome):
    plt.figure(figsize=(12, 10))
    
    # Calcular a Temperatura Média
    df['Temp Média'] = (df['Temp Max (max) (max)'] + df['Temp Min (min) (min)']) / 2

    # Gráfico de Temperatura
    plt.subplot(2, 2, 1)
    plt.plot(df['Data'], df['Temp Max (max) (max)'], label='Temperatura Máxima', color='red')
    plt.plot(df['Data'], df['Temp Min (min) (min)'], label='Temperatura Mínima', color='blue')
    plt.plot(df['Data'], df['Temp Média'], label='Temperatura Média', color='green', linestyle='--')
    plt.axhline(y=25, color='orange', linestyle='--', label='Temperatura Máxima para Kiwi (25°C)')
    plt.axhline(y=5, color='purple', linestyle='--', label='Temperatura Mínima para Kiwi (5°C)')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.title(f'Temperaturas em {cidade_nome}')
    plt.legend()
    
    # Verificar se a precipitação está sendo reportada por dia ou não
    if 'Precipitacao Total (soma) (sum)' in df.columns:
        # Gráfico de Precipitação com linha ajustada
        plt.subplot(2, 2, 2)
        plt.plot(df['Data'], df['Precipitacao Total (soma) (sum)'], label='Precipitação', color='green')
        
        # Verificar se a precipitação total está em base mensal, então converter para diária
        precip_media_diaria = 125 / 30  # Dividir 125mm/mês por 30 dias do mês
        
        # Ajuste da linha de precipitação para valores diários calculados
        plt.axhline(y=precip_media_diaria, color='purple', linestyle='--', label=f'Precipitação Diária {precip_media_diaria:.2f}mm')
        plt.xlabel('Data')
        plt.ylabel('Precipitação (mm)')
        plt.title(f'Precipitação em {cidade_nome}')
        plt.legend()

    # Gráfico de Umidade Relativa ajustada entre 60% e 90%
    plt.subplot(2, 2, 3)
    if 'Umidade Relativa (mean) (mean)' in df.columns:
        plt.plot(df['Data'], df['Umidade Relativa (mean) (mean)'], label='Umidade Relativa', color='brown')
        plt.axhline(y=90, color='orange', linestyle='--', label='Limite Máximo 90%')
        plt.axhline(y=60, color='red', linestyle='--', label='Limite Mínimo 60%')
        plt.xlabel('Data')
        plt.ylabel('Umidade (%)')
        plt.title(f'Umidade Relativa em {cidade_nome}')
        plt.legend()

    plt.tight_layout()
    plt.show()

# Carregar os dados de cada cidade
cidade_lages = carregar_json("dados_em_json/lages.json")
cidade_farroupilha = carregar_json("dados_em_json/farroupilha.json")
cidade_sao_mateus = carregar_json("dados_em_json/são_mateus_do_sul.json")

# Converter os dados de cada cidade em DataFrames
df_lages = extrair_dados_json(cidade_lages)
df_farroupilha = extrair_dados_json(cidade_farroupilha)
df_sao_mateus = extrair_dados_json(cidade_sao_mateus)

# Analisar estatísticas das variáveis de clima para cada cidade
estatisticas_lages = analise_estatisticas(df_lages)
estatisticas_farroupilha = analise_estatisticas(df_farroupilha)
estatisticas_sao_mateus = analise_estatisticas(df_sao_mateus)

# Exibir as estatísticas
print("Estatísticas Lages:", estatisticas_lages)
print("Estatísticas Farroupilha:", estatisticas_farroupilha)
print("Estatísticas São Mateus do Sul:", estatisticas_sao_mateus)

# Analisar condições climáticas para cada cidade
condicoes_lages = analisar_condicoes_colheita(df_lages)
condicoes_farroupilha = analisar_condicoes_colheita(df_farroupilha)
condicoes_sao_mateus = analisar_condicoes_colheita(df_sao_mateus)

# Exibir as condições climáticas para cada cidade
print("Cidade Lages - Temperatura Máxima: {:.2f}, Temperatura Mínima: {:.2f}, Precipitação Total: {:.2f}".format(*condicoes_lages))
print("Cidade Farroupilha - Temperatura Máxima: {:.2f}, Temperatura Mínima: {:.2f}, Precipitação Total: {:.2f}".format(*condicoes_farroupilha))
print("Cidade São Mateus do Sul - Temperatura Máxima: {:.2f}, Temperatura Mínima: {:.2f}, Precipitação Total: {:.2f}".format(*condicoes_sao_mateus))

# Inferir impacto para cada cidade
impacto_lages = inferir_impacto_na_producao(*condicoes_lages)
impacto_farroupilha = inferir_impacto_na_producao(*condicoes_farroupilha)
impacto_sao_mateus = inferir_impacto_na_producao(*condicoes_sao_mateus)

# Exibir impacto da produção para cada cidade
print("Impacto Lages:", impacto_lages)
print("Impacto Farroupilha:", impacto_farroupilha)
print("Impacto São Mateus do Sul:", impacto_sao_mateus)

# Plotar gráficos para cada cidade
plotar_graficos(df_lages, "Lages")
plotar_graficos(df_farroupilha, "Farroupilha")
plotar_graficos(df_sao_mateus, "São Mateus do Sul")
