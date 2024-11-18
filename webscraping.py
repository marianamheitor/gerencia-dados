# Cidades: - Antônio Olinto (Paraná)
#          - Campo Belo do Sul (Santa Catarina)
#          - Farroupilha (Rio Grande do Sul)

# Características: - Nome da cidade
#                  - Temperatura
#                  - Chuva
#                  - Vento
#                  - Umidade

# URLs: - https://www.climatempo.com.br
#       - https://portal.inmet.gov.br/dadoshistoricos

import re
import requests
from bs4 import BeautifulSoup


# url_request = requests.get('https://www.climatempo.com.br/previsao-do-tempo/cidade/4215/antonioolinto-pr')
# url_request = requests.get('https://www.climatempo.com.br/previsao-do-tempo/cidade/4577/campobelodosul-sc')
url_request = requests.get('https://www.climatempo.com.br/previsao-do-tempo/cidade/356/farroupilha-rs')

# Verifica se a conexão URL foi estabelecida com sucesso
if (url_request.status_code == 200): # ou if (url_request.ok)
    print('Conexão estabelecida.')

    # Busca o conteúdo da página, passando-o à variável
    url_content = BeautifulSoup(url_request.content, 'html.parser')
    weather_content = url_content.find('ul', class_='variables-list')

    # Temperatura (meta)
    # print(f"Temperatura mínima: {url_content.find('meta',{'name':'tmin'}).get('content')}")
    # print(f"Temperatura máxima: {url_content.find('meta',{'name':'tmax'}).get('content')}")
    # print(f"Temperatura atual: {url_content.find('meta',{'name':'tmomento'}).get('content')}")


    # Extrai os atributos desejados da página
    extracted_attributes = weather_content.find_all('li',class_='item')
    extracted_values = []

    # Formata os atributos extraídos
    for attribute in extracted_attributes[:4]:
        aux_value = [value for value in re.split("\n|\t|-", attribute.text) if value != '']
        extracted_values.append(aux_value)
    print(extracted_values)

else:
    print('Erro na conexão.')
