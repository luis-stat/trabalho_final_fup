from datetime import datetime

def verificar_sobreposicao(inicio1: datetime, fim1: datetime, inicio2: datetime, fim2: datetime) -> bool:
    return max(inicio1, inicio2) < min(fim1, fim2)

def validar_intervalo(inicio: datetime, fim: datetime) -> bool:
    return inicio < fim

def validar_data_futura(inicio: datetime) -> bool:
    return inicio >= datetime.now()