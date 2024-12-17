import json
import pandas as pd
import matplotlib.pyplot as plt


def plot_weather(city):
    with open(f'../dataset_json/{city.replace(" ", "_").lower()}_15_dias.json') as json_file:
        json_data = json.load(json_file)

    columns = []
    for element in json_data[1:]:
        del element["Direção do Vento"]
        for key, value in element.items():
            if key not in columns:
                columns.append(key)
            if key == "Data":
                element[key] = int(value)
            elif key == "Total de Precipitação":
                element[key] = float(value[:-2])
            elif key == "Velocidade do Vento":
                element[key] = float(value[:-4])
            else:
                element[key] = float(value[:-1])


    df_data = pd.DataFrame(json_data)

    # Temperatura
    plt.plot(df_data[columns[0]],df_data[columns[1]], label='Temperatura Mínima', color='blue')
    plt.plot(df_data[columns[0]],df_data[columns[2]], label='Temperatura Máxima', color='red')
    plt.axhline(y=7, color='purple', linestyle='--', label='Temperatura Mínima para Kiwi (7°C)')
    plt.axhline(y=25, color='orange', linestyle='--', label='Temperatura Máxima para Kiwi (25°C)')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.title(f'Temperatura em {city}')
    plt.legend()
    plt.show()

    # Precipitação
    plt.plot(df_data[columns[0]],df_data[columns[3]], label='Precipitação', color='green')
    plt.axhline(y=125 / 30, color='purple', linestyle='--', label=f'Precipitação Diária {125 / 30:.1f}mm')
    plt.xlabel('Data')
    plt.ylabel('Precipitação (mm)')
    plt.title(f'Precipitação em {city}')
    plt.legend()
    plt.show()

    # Umidade
    plt.plot(df_data[columns[0]],df_data[columns[6]], label='Umidade Mínima', color='blue')
    plt.plot(df_data[columns[0]],df_data[columns[7]], label='Umidade Máxima', color='red')
    plt.axhline(y=60, color='purple', linestyle='--', label='Limite Mínimo 60%')
    plt.axhline(y=90, color='orange', linestyle='--', label='Limite Máximo 90%')
    plt.xlabel('Data')
    plt.ylabel('Umidade (%)')
    plt.title(f'Umidade em {city}')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    cities = ['Farroupilha', 'Lages', 'São Mateus do Sul']
    for city in cities:
        plot_weather(city)
