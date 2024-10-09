import pandas as pd

# Cargar los CSV en DataFrames
df_10 = pd.read_csv('10.csv')  # Este contiene la lista completa de productos
df_20 = pd.read_csv('30.csv')  # Este contiene la lista de SKU y precios

# Filtrar las filas de 10.csv donde el valor de la columna 'Superior' coincida con algún SKU de 20.csv
df_filtered = df_10[df_10['Superior'].isin(df_20['SKU'])]

# Combinar los dos DataFrames en base a la columna 'Superior' en df_10 y 'SKU' en df_20
df_combined = df_filtered.merge(df_20, how='left', left_on='Superior', right_on='SKU')

# Comprobar qué columnas existen después del merge
print("Columnas disponibles después del merge:", df_combined.columns)

# Si las columnas existen, actualizamos los precios; de lo contrario, revisamos qué está pasando
if 'Precio rebajado' in df_combined.columns and 'Precio normal' in df_combined.columns:
    # Actualizar los precios con los valores del archivo 20.csv
    df_combined['Precio rebajado'] = df_combined['Precio rebajado']
    df_combined['Precio normal'] = df_combined['Precio normal']
else:
    print("Las columnas de precios no se encontraron.")

# Guardar el resultado en un nuevo archivo CSV
df_combined.to_csv('filtrado_con_precios.csv', index=False)

print("Archivo 'filtrado_con_precios.csv' generado con los precios actualizados.")
