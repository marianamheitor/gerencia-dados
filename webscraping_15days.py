# Cidades: - São Mateus do Sul (Paraná)
#          - Lages (Santa Catarina)
#          - Farroupilha (Rio Grande do Sul)

# Características: - Dia
#                  - Temperatura
#                  - Chuva
#                  - Vento
#                  - Umidade


import re
import json
import requests
from bs4 import BeautifulSoup


def extract_weather_info(city, code):
    print(f"Extraindo informações sobre a cidade {city} ({code}).")
    extracted_attributes = {}

    url_request = requests.get(f'https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/{code}')
    # Verifica se a conexão URL foi estabelecida com sucesso
    if (url_request.status_code == 200): # ou if (url_request.ok)
        print("Conexão estabelecida.")

        # Busca o conteúdo da página, passando-o à variável
        url_content = BeautifulSoup(url_request.content, 'html.parser')

        # Busca o conteúdo dos 15 dias de previsão
        days_content = url_content.find_all('section', class_='accordion-card -daily-infos _border-bl-light-1')

        for day_content in days_content:
            # Busca e extrai a data do dia a ser analisado
            extracted_day = day_content.find_all('div',class_='date-inside-circle')
            day_value = extracted_day[0].text.split()

            print(f"Analisando dia {day_value[0]} - {day_value[1]}.")

            # Busca os atributos do clima do dia a ser analisado
            extracted_weather = day_content.find_all('div',class_=re.compile('^-gray _flex'))
            extracted_attributes[day_value[0]] = []

            # Extrai e armazena o valor dos atributos da página
            for attribute in extracted_weather:
                text_value = attribute.text.split()
                text_value = [value for value in text_value if value != '-']
                extracted_attributes[day_value[0]].append(text_value)

            print("Atributos extraídos.")
        
        return (extracted_attributes, f'https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/{code}')

    else:
        print("Erro na conexão.")


def save_json(city, extracted_attributes):
    # Formata os dados para salvar no JSON
    json_data = [{"Nome da cidade":city, "URL":extracted_attributes[1]}]
    attribute_name = [["Temperatura Mínima", "Temperatura Máxima"],
                      ["Total de Precipitação", "Chance de Precipitação"],
                      ["Direção do Vento", "Velocidade do Vento"],
                      ["Umidade Mínima", "Umidade Máxima"]]
    for day, attribute in extracted_attributes[0].items():
        current_attribute = {}

        # Atributos que serão salvos em JSON
        current_attribute['Data'] = day
        for index, info in enumerate(attribute):
            current_attribute[attribute_name[index][0]] = info[0]
            current_attribute[attribute_name[index][1]] = info[1]

        # Adiciona os valores dos atributos da data extraída
        json_data.append(current_attribute)

    # Salva dados em formato JSON
    json_path = f'{city.replace(" ", "_").lower()}_15_dias.json'
    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)
    print(f"JSON para {city} gerado em {json_path}")


if __name__ == '__main__':
    # Cidade de interesse e código correspondente 
    cities_codes = {
        "Farroupilha": "356",
        "Lages": "382",
        "São Mateus do Sul": "2917"
    }

    for city, code in cities_codes.items():
        extracted_attributes = extract_weather_info(city, code)
        save_json(city, extracted_attributes)
