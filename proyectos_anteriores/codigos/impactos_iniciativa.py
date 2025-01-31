""" Esta es una clase para sacar los impactos de una iniciativa. Supone que los precios de 
la iniciativa se leen desde un archivo externo."""

# importar librerías
import pandas as pd
import numpy as np
from utils import ingresos_financieros, calcular_cuota, meses_entre_fechas, reservas
from dateutil.relativedelta import relativedelta
from datetime import datetime

class ImpactosIniciativa:
    def __init__(self, creditos: pd.DataFrame,
                        monto: str,
                        plazo, 
                        tasa: str, 
                        fec_apertura: str, 
                        neto: str,
                        precios: pd.DataFrame=None,):
        self.creditos = creditos
        self.precios = precios
        self.monto = monto      # es el monto bruto
        self.neto = neto
        self.plazo = plazo
        self.tasa = tasa
        self.fec_apertura = fec_apertura

    # Método para leer precios desde una tabla externa
    # prec1 hace referencia al precificador de fila (monto o prec1 en las tablas)
    # prec2 hace referencia al precificador de columna (prec2 generalmente)
    # cota_prec1 es la cota para el precificador de fila (montos de 500k, RCI 59, etc)

    # Método para saber si el recrédito implicaba reservas o no
    def flag15_total(self, no_credito: float, cols_saldos: str) -> int:
        creds_temp = self.creditos.groupby(by=no_credito)[cols_saldos].min().reset_index(name="MIN SALDO")
        self.creditos = pd.merge(self.creditos, creds_temp, on=no_credito, how="left")
        self.creditos["PAGA RESERVAS"] = np.where(self.creditos["MIN SALDO"] < 0.15, 1, 0)

    # Método para sacar ingresos financieros recibidos, construye una columnad e los ingresos
    def ingresos_recibidos(self, nombre: str, meses_fijo: bool):
        if not meses_fijo:
            self.creditos["MESES TRANSCURRIDOS"] = self.creditos.apply(lambda x: meses_entre_fechas(x[self.fec_apertura], datetime.today()), axis=1)
            self.creditos[f"INGRESOS {nombre}"] = self.creditos.apply(lambda x: ingresos_financieros(x[self.monto], x[self.tasa]/1200, x[self.plazo], x["MESES TRANSCURRIDOS"]), axis=1)        
        if meses_fijo:
            self.creditos["MESES TRANSCURRIDOS"] = 6
            self.creditos[f"INGRESOS {nombre}"] = self.creditos.apply(lambda x: ingresos_financieros(x[self.monto], x[self.tasa]/1200, x[self.plazo], x["MESES TRANSCURRIDOS"]), axis=1)
    
    # Método para sacar reservas
    def reservas_reestructuracion(self, nombre: str, recredito: bool):
        self.creditos[f"RESERVAS {nombre}"] = self.creditos.apply(lambda x: reservas(recredito) * x[self.monto], axis=1)
        
    # Método para sacar costos pasivos
    def pasivos(self, nombre: str):
        self.creditos[f"PASIVOS {nombre}"] = (0.0653 + 0.0025) / (1 - 0.146) * self.creditos[self.monto]

    # Método para calcular el margen financiero
    def margen_financiero(self, nombre: str, reservas: bool):
        self.pasivos(nombre)
        if reservas: 
            self.creditos[f"MF {nombre}"] = self.creditos[f"INGRESOS {nombre}"] - self.creditos[f"RESERVAS {nombre}"] - self.creditos[f"PASIVOS {nombre}"]
        if not reservas:
            self.creditos[f"MF {nombre}"] = self.creditos[f"INGRESOS {nombre}"] - self.creditos[f"PASIVOS {nombre}"]