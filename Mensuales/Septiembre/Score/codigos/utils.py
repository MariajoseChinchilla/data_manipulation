#### funciones útiles para el escenario de simulación de quitar codeudor y cambiar corte de score
from scipy.stats import t
import numpy as np

# función para calcular proporción
# devuelve los estadisticos en un diccioario con sus nombres y a dos decimales
def estadisticos_resumen(df, col_mora:str, valor_si_mora, col_bruto: str,
                         col_neto: str, col_rci: str) -> dict:
    estadisticos = {}
    tamaño_muestra = len(df)
    proporcion_mora = len(df[df[col_mora] == valor_si_mora]) / len(df)
    desembolso_bruto_promedio_poblacional = df[col_bruto].mean()
    desembolso_neto_promedio_poblacional = df[col_neto].mean()
    desembolso_bruto_promedio_morosos = df[df[col_mora] == valor_si_mora][col_bruto].mean()
    desembolso_neto_promedio_morosos = df[df[col_mora] == valor_si_mora][col_neto].mean()
    desembolso_bruto_promedio_no_morosos = df[df[col_mora] != valor_si_mora][col_bruto].mean()
    desembolso_neto_promedio_no_morosos = df[df[col_mora] != valor_si_mora][col_neto].mean()
    cantidad_morosos = len(df[df[col_mora] == valor_si_mora])
    porcentaje_clientes_morosos = proporcion_mora * 100
    rci_no_morosos = df[df[col_mora] != valor_si_mora][col_rci].mean()
    rci_morosos = df[df[col_mora] == valor_si_mora][col_rci].mean()

    # agregar a diccionario
    estadisticos["Tamaño de la muestra"] = tamaño_muestra
    estadisticos["Proporción mora"] = proporcion_mora
    estadisticos["Desembolso bruto promedio poblacional"] = round(desembolso_bruto_promedio_poblacional, 2)
    estadisticos["Desembolso neto promedio poblacional"] = round(desembolso_neto_promedio_poblacional, 2)
    estadisticos["Desembolso bruto promedio morosos"] = round(desembolso_bruto_promedio_morosos, 2)
    estadisticos["Desembolso neto promedio morosos"] = round(desembolso_neto_promedio_morosos, 2)
    estadisticos["Desembolso bruto promedio no morosos"] = round(desembolso_bruto_promedio_no_morosos, 2)
    estadisticos["Desembolso neto promedio no morosos"] = round(desembolso_neto_promedio_no_morosos, 2)
    estadisticos["Cantidad de personas con mora"] = cantidad_morosos
    estadisticos["Porcentaje de clientes con mora"] = round(porcentaje_clientes_morosos, 2)
    estadisticos["RCI promedio de clientes no morosos"] = round(rci_no_morosos, 2)
    estadisticos["RCI promedio de clientes morosos"] = round(rci_morosos, 2)

    return estadisticos


# función para analizar impacto de las iniciativas
def impacto_cambio(df, nuevo_score: int, antiguo_score: int, col_mora: str, valor_si_mora, 
                   col_bruto: str, col_neto: str, col_score: str, significancia: float) -> dict:
    
    # Justificado usar distribución normal por tamaño de la musetra y TLC
    impactos = {}

    # datos actuales
    try:
        proporcion_actual = len(df[df[col_mora] == valor_si_mora]) / len(df)
    except: 
        proporcion_actual = 0
    try:
        prop_mora_con_cod = len(df[(df[col_mora] == valor_si_mora) & (df[col_score] <= antiguo_score)]) / len(df[col_score] <= antiguo_score)
    except:
        prop_mora_con_cod = 0
    try:
        prop_mora_sin_cod = len(df[(df[col_score] > antiguo_score) & (df[col_mora] == valor_si_mora)]) / len(df[df[col_score] > antiguo_score])
    except:
        prop_mora_sin_cod = 0
    try:
        prop_codeudor = len(df[df[col_score] <= antiguo_score]) / len(df)
    except:
        prop_codeudor = 0
    clientes_viejos_sin_codeudor = len(df[df[col_score] > antiguo_score])

    # nuevas: estimaciones
    clientes_nuevos_codeudor = len(df[df[col_score] < nuevo_score])
    clientes_nuevos_sin_cod = len(df[df[col_score] >= nuevo_score]) - clientes_viejos_sin_codeudor
    desembolso_neto_prom_codeudor = df[df[col_score] <= nuevo_score][col_neto].mean()
    desembolso_bruto_prom_codeudor = df[df[col_score] <= nuevo_score][col_bruto].mean()
    desviacion_neto_codeudor = df[df[col_score] <= nuevo_score][col_neto].std()
    desviacion_bruto_codeudor = df[df[col_score] <= nuevo_score][col_bruto].mean()
    desembolso_neto_prom_sin_codeudor = df[df[col_score] > nuevo_score][col_neto].mean()
    desembolso_bruto_prom_sin_codeudor = df[df[col_score] > nuevo_score][col_bruto].mean()
    desviacion_neto_sin_codeudor = df[df[col_score] > nuevo_score][col_neto].std()
    desviacion_bruto_sin_codeudor = df[df[col_score] > nuevo_score][col_bruto].mean()
    proporcion_mora_nueva = (prop_mora_con_cod * clientes_nuevos_codeudor + prop_mora_sin_cod * clientes_nuevos_sin_cod) / len(df) + proporcion_actual
    aumento_mora = proporcion_mora_nueva - proporcion_actual
    porcentaje_aumento_clientes = clientes_nuevos_sin_cod / len(df)
    
    t_s = abs(t.ppf(significancia/2, len(df) - 1))
    error_neto = t_s * desviacion_neto_codeudor / np.sqrt(len(df))
    error_bruto = t_s * desviacion_bruto_codeudor / np.sqrt(len(df))
    intervalo_neto_codeudor = (desembolso_neto_prom_codeudor - error_neto, desembolso_neto_prom_codeudor + error_neto)
    intervalo_bruto_codeudr = (desembolso_bruto_prom_codeudor - error_bruto, desembolso_bruto_prom_codeudor + error_bruto)

    error_neto_sin = t_s * desviacion_neto_sin_codeudor / np.sqrt(len(df))
    error_bruto_sin = t_s * desviacion_bruto_sin_codeudor / np.sqrt(len(df))
    intervalo_neto_sin_codeudor = (desembolso_neto_prom_sin_codeudor - error_neto, desembolso_neto_prom_sin_codeudor + error_neto_sin)
    intervalo_bruto_sin_codeudr = (desembolso_bruto_prom_sin_codeudor - error_bruto_sin, desembolso_bruto_prom_sin_codeudor + error_bruto_sin)
    
    nuevo_desembolso_neto_sin_cod = (intervalo_neto_sin_codeudor[0] * clientes_nuevos_sin_cod, intervalo_neto_sin_codeudor[1] * clientes_nuevos_sin_cod)
    nuevo_bruto_sin_cod = (intervalo_bruto_sin_codeudr[0] * clientes_nuevos_sin_cod, intervalo_bruto_sin_codeudr[1] * clientes_nuevos_sin_cod)
    reservas_estimadas = (nuevo_bruto_sin_cod[0]*0.05*0.45, nuevo_bruto_sin_cod[1]*0.05*0.45)
    
    try:
        probabilidad_mora_cliente_codeudor = prop_mora_con_cod / prop_codeudor
    except:
        probabilidad_mora_cliente_codeudor = 0
    try:
        probabilidad_mora_sin_codeudor = proporcion_actual / (1 - prop_codeudor)
    except:
        probabilidad_mora_sin_codeudor = 0
    try:
        probabilidad_total_mora = probabilidad_mora_sin_codeudor + prop_mora_con_cod
    except: 
        probabilidad_total_mora = 0
    # guardar diccionario
    impactos["Clientes nuevos con codeudor"] = clientes_nuevos_codeudor
    impactos["Clientes nuevos sin codeudor"] = clientes_nuevos_sin_cod
    impactos["Aumento porcentual clientes"] = porcentaje_aumento_clientes 
    impactos["Nueva proporción de mora"] = proporcion_mora_nueva
    impactos["Aumento porcentual mora"] = aumento_mora 

    impactos["Desembolso neto promedio esperado con codeudor"] = intervalo_neto_codeudor
    impactos["Desembolso bruto promedio esperado con codeudor"] = intervalo_bruto_codeudr
    impactos["Desembolso bruto total sin codeudor"] = nuevo_bruto_sin_cod

    impactos["Desembolso neto promedio esperado sin codeudor"] = intervalo_neto_sin_codeudor
    impactos["Desembolso bruto promedio esperado sin codeudor"] =  intervalo_bruto_sin_codeudr
    impactos["Desembolso neto total sin codeudor"] = nuevo_desembolso_neto_sin_cod

    impactos["Reservas estimadas"] = reservas_estimadas
    impactos["Probabilidad de mora con codeudor"] = probabilidad_mora_cliente_codeudor
    impactos["Probabilidad de mora sin codeudor"] = probabilidad_mora_sin_codeudor
    impactos["Probabilidad total de mora"] = probabilidad_total_mora

    return impactos
    