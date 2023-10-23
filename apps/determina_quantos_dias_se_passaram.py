from datetime import datetime
from apps.timestamp_to_datetime import parse_timestamp

def calcular_dias_passados(data):
    # Obtenha a data e hora atual
    data = parse_timestamp(data)
    data_atual = datetime.now()

    # Calcule a diferença entre as duas datas
    diferenca = data_atual - data

    # Extraia o número de dias e horas da diferença
    dias_passados = diferenca.days

    response = dias_passados
    return response

# Exemplo de uso:

