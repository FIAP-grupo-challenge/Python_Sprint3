from flask import make_response

from apps.determina_quantos_dias_se_passaram import calcular_dias_passados


def formatar_response_grafico(dados, type, plant_id,):
    valid_type = ["temp", "humi", "light", "ph"]
    response = {}
    if type not in valid_type:
        response["response"] = "type invalido"
        response = make_response(response)
        response.mimetype = "raw/json"
        return response
    else:
        if not dados:
            response["response"] = "planta sem dados"
        else:

            number_of_elements_array = []
            date_array = []
            light_array = []
            ph_array = []
            temp_array = []
            humi_array = []

            for dado in dados:
                data = calcular_dias_passados(dado[7])

                if data not in date_array:
                    date_array.append(data)
                    temp_array.append(int(dado[2]))
                    humi_array.append(int(dado[3]))
                    light_array.append(int(dado[4]))
                    ph_array.append(float(dado[5]))
                    number_of_elements_array.append(1)
                else:
                    temp_array[date_array.index(data)] += int(dado[2])
                    humi_array[date_array.index(data)] += int(dado[3])
                    light_array[date_array.index(data)] += int(dado[4])
                    ph_array[date_array.index(data)] += float(dado[5])
                    number_of_elements_array[date_array.index(data)] += 1

            for i in range(len(date_array)):
                temp_array[i] = round(temp_array[i]/number_of_elements_array[i],2)
                humi_array[i] = round(humi_array[i]/number_of_elements_array[i],2)
                light_array[i] = round(light_array[i]/number_of_elements_array[i],2)
                ph_array[i] = round(ph_array[i]/number_of_elements_array[i],2)

            print(f"light_array :{light_array}")
            print(f"temp_array :{temp_array}")
            print(f"humi_array :{humi_array}")
            print(f"ph_array :{ph_array}")
            print(f"date_array :{date_array}")
            print(f"number_of_elements_array :{number_of_elements_array}")

            response = {
                "temp": {
                    "response": "201",
                    "id": plant_id,
                    "dados": {
                        "info": temp_array,
                        "date": date_array
                    }
                },
                "humi": {
                    "response": "201",
                    "id": plant_id,
                    "dados": {
                        "info": humi_array,
                        "date": date_array
                    }
                },
                "light": {
                    "response": "201",
                    "id": plant_id,
                    "dados": {
                        "info": light_array,
                        "date": date_array
                    }
                },
                "ph": {
                    "response": "201",
                    "id": plant_id,
                    "dados": {
                        "info": ph_array,
                        "date": date_array
                    }
                }
            }

            response = make_response(response[type])
            response.mimetype = "raw/json"

            return response