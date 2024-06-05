# función que verifica si un crédito ya cumplió el 15% de pago a capital
def cumple_15(saldo: float) -> int:
    if saldo < 0.15:
        return 0
    elif saldo >= 0.15:
        return 1
    
# función que calcula la cuota de un crédito
def calcular_cuota(monto: float, tasa: float, plazo: int) -> float:
    cuota = (monto * tasa * (1 + tasa)**plazo) / ((1 + tasa)**plazo - 1)
    return cuota

def ingresos_financieros(monto: float, tasa: float, plazo: int, n: int) -> float:
    cuota = calcular_cuota(monto, tasa, plazo)
    ingresos = (monto - cuota / tasa) * ((1 + tasa)**n - 1) + cuota * n
    return ingresos

# función que calcula el monto máximo para llegar a un nivel de RCI con la tasa dada
def calcular_monto_a_rci(tasa: float, rci_deseado: float, 
                         plazo: int, rci_actual: float,
                         salario: float) -> float:
    num = (rci_deseado - rci_actual) * ((1 + tasa)**plazo - 1) * salario
    den = tasa * (1 + tasa)**plazo
    monto = num / den
    return monto

# función que compara si un monto es menor a otro
def comparar_montos(monto1: float, monto2: float) -> int:
    if monto1 <= monto2:
        return 1
    return 0

# funcion que calcula las reservas por reestructuracion
def reservas(reestructuracion: bool) ->  float:
    if reestructuracion:
        reservas = 0.05 * 0.45
    else:
        reservas = 0.036 * 0.45
    return reservas

# funcion para calcular la tasa minima para dejar a cero el margen
def tasa_minima(reservas):
    pasivos = (0.08 + 0.0025) / (1 - 0.146)
    return pasivos + reservas

# funcion que calcula la tasa maxima del cliente para llegar a un nivel de RCI
def tasa_maxima(rci: float, cota: float) -> float:
    return cota - rci