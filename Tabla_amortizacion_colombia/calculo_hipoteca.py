import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calcular_nueva_amortizacion(saldo_actual, tasa_ea, cuota_deseada, fecha_inicio):
    """
    Calcula la nueva tabla de amortización con la cuota incrementada
    """
    resultados = []
    saldo = saldo_actual
    tasa_mensual = (1 + tasa_ea)**(1/12) - 1
    fecha = datetime.strptime(fecha_inicio, "%d/%m/%Y")
    periodo = 8  # Iniciamos en la cuota 8
    
    while saldo > 0:
        # Cálculos mensuales
        interes = saldo * tasa_mensual
        seguro_vida = saldo * 0.000224  # Según historial de pagos
        seguro_terremoto = 22792  # Valor fijo según historial
        
        cuota_base = cuota_deseada - seguro_vida - seguro_terremoto
        capital = cuota_base - interes
        
        # Actualizar saldo
        saldo = saldo - capital
        
        resultados.append({
            'PERÍODO': periodo,
            'FECHA': fecha.strftime("%d/%m/%Y"),
            'Interes efectiva mensual': f"{tasa_mensual:.2%}",
            'Intereses mensuales': round(interes),
            'Valor Capital': round(capital),
            'Seguro vida': round(seguro_vida),
            'Seguro terremoto': seguro_terremoto,
            'Total cuota': round(cuota_deseada),
            'Deuda total': round(max(0, saldo))
        })
        
        fecha = fecha + timedelta(days=30)
        periodo += 1
        
        if saldo <= 0:
            break
    
    return pd.DataFrame(resultados)

# Datos del crédito
SALDO_ACTUAL = 105496315
TASA_EA = 0.1014
CUOTA_DESEADA = 2700000
FECHA_INICIO = "22/11/2024"

# Generar nueva tabla
nueva_tabla = calcular_nueva_amortizacion(
    saldo_actual=SALDO_ACTUAL,
    tasa_ea=TASA_EA,
    cuota_deseada=CUOTA_DESEADA,
    fecha_inicio=FECHA_INICIO
)

# Calcular totales
total_intereses = nueva_tabla['Intereses mensuales'].sum()
total_capital = nueva_tabla['Valor Capital'].sum()
total_seguros = nueva_tabla['Seguro vida'].sum() + nueva_tabla['Seguro terremoto'].sum()
meses_totales = len(nueva_tabla)

# Imprimir resumen
print("\nResumen del nuevo plan de pagos:")
print(f"Número total de cuotas: {meses_totales}")
print(f"Total intereses a pagar: ${total_intereses:,.0f}")
print(f"Total capital a pagar: ${total_capital:,.0f}")
print(f"Total seguros a pagar: ${total_seguros:,.0f}")

# Guardar en Excel
ruta_archivo = "~/Desktop/nueva_tabla_amortizacion.xlsx"
nueva_tabla.to_excel(ruta_archivo, index=False)
print(f"\nSe ha guardado la tabla en: {ruta_archivo}")