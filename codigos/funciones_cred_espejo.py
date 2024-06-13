from utils import calcular_monto_a_rci

# Se asume que la lista de créditos viene en el formato (monto, tasa, plazo, categoría, cumple)
def elegir_creditos_a_consolidar(tipo: str, creditos: list, monto_max: float):
    consolidar = []
    suma_consolidacion = 0
    
    if tipo == "Total":
        return creditos
    
    if tipo == "Categoría":
        # Ordenar descendente por categoría
        creditos_temp = sorted(creditos, key=lambda x: x[3], reverse=True)
    elif tipo == "15%":
        # Ordenar para priorizar los que ya cumplieron el 15%
        creditos_temp = sorted(creditos, key=lambda x: x[4], reverse=True)
    else:
        raise ValueError("Tipo de consolidación no válido")
    
    for cred in creditos_temp:
        if suma_consolidacion + cred[0] > monto_max:
            break
        suma_consolidacion += cred[0]
        consolidar.append(cred)
    
    return consolidar

# Función para calcular TPP (sirve para lo de RCI 60)
def logica_consolidacion(tipo: str, creditos: list, rci: float, salario: float):
    try:
        if tipo == "Total":
            tpp = sum(cred[0] * cred[1] for cred in creditos) / sum(cred[0] for cred in creditos)
            monto_max = calcular_monto_a_rci(tpp, 60, 144, rci, salario)
            montos_consolidar = elegir_creditos_a_consolidar("Total", creditos, monto_max)
    except:
        pass