import pandas as pd
import numpy as np

def crear_tabla_amortizacion(monto_inicial, tasa_ea, cuota_mensual, plazo_meses):
    # Convertir tasa EA a mensual
    tasa_mensual = (1 + tasa_ea) ** (1/12) - 1
    
    # Crear listas para almacenar los valores
    saldo_capital = []
    cuota = []
    interes = []
    abono_capital = []
    
    # Inicializar saldo
    saldo_actual = monto_inicial
    
    for mes in range(1, plazo_meses + 1):
        # Calcular interés del mes
        interes_mes = saldo_actual * tasa_mensual
        
        # Calcular abono a capital
        abono_capital_mes = cuota_mensual - interes_mes
        
        # Actualizar saldo
        saldo_actual = saldo_actual - abono_capital_mes
        
        # Almacenar valores
        saldo_capital.append(saldo_actual)
        cuota.append(cuota_mensual)
        interes.append(interes_mes)
        abono_capital.append(abono_capital_mes)
    
    # Crear DataFrame
    df = pd.DataFrame({
        'Cuota_N': range(1, plazo_meses + 1),
        'Cuota_Mensual': cuota,
        'Intereses': interes,
        'Abono_Capital': abono_capital,
        'Saldo_Capital': saldo_capital
    })
    
    # Formatear números
    df = df.round(2)
    
    return df

# Crear tabla para la cuota de $1,775,000 (escenario a 10 años)
tabla_10_anos = crear_tabla_amortizacion(
    monto_inicial=104800000,  # Saldo después de 6 cuotas
    tasa_ea=0.104,
    cuota_mensual=1775000,
    plazo_meses=120
)

# Formatear para exportar a Excel
tabla_10_anos.to_excel('Amortizacion_Credito_10_anos.xlsx', index=False)

# Mostrar primeros 12 meses
print("\nPrimeros 12 meses del crédito:")
print(tabla_10_anos.head(12).to_string())

# Mostrar resumen
print("\nResumen del crédito:")
print(f"Total pagado en intereses: ${tabla_10_anos['Intereses'].sum():,.2f}")
print(f"Total pagado en capital: ${tabla_10_anos['Abono_Capital'].sum():,.2f}")
print(f"Total pagado: ${tabla_10_anos['Cuota_Mensual'].sum():,.2f}")