# Cidades: - Antônio Olinto (Paraná)
#          - Campo Belo do Sul (Santa Catarina)
#          - Farroupilha (Rio Grande do Sul)

# Características: - Nome da cidade
#                  - Dia
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
url_request = requests.get('https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/356/farroupilha-rs')

# Verifica se a conexão URL foi estabelecida com sucesso
if (url_request.status_code == 200): # ou if (url_request.ok)
    print('Conexão estabelecida.')

    # Busca o conteúdo da página, passando-o à variável
    url_content = BeautifulSoup(url_request.content, 'html.parser')

    # Busca o conteúdo dos 15 dias de previsão
    days_content = url_content.find_all('section', class_='accordion-card -daily-infos _border-bl-light-1')

    for day_content in days_content:
        # Busca a data do dia a ser analisado
        extracted_day = day_content.find_all('div',class_='date-inside-circle')
        day_value = []
        # Extrai a data da página
        for day in extracted_day:
            text_value = day.text.split()
            day_value = text_value
        print(day_value)

        # Busca os atributos do clima do dia a ser analisado
        extracted_weather = day_content.find_all('div',class_=re.compile('^-gray _flex'))
        extracted_attributes = []
        # Extrai o valor dos atributos da página
        for attribute in extracted_weather:
            text_value = attribute.text.split()
            text_value = [value for value in text_value if value != '-']
            extracted_attributes.append(text_value)
        print(extracted_attributes)
        
    

else:
    print('Erro na conexão.')
