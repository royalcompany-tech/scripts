import pandas as pd

# Cargar los CSV en DataFrames
df1 = pd.read_csv('1.csv')  # Este tiene los campos SKU y Publicado
df2 = pd.read_csv('2.csv')  # Este es el que quieres procesar

# Crear un diccionario con los valores de SKU y Publicado de 1.csv
dict_1 = df1.set_index('SKU')['Publicado'].to_dict()

# Función para actualizar el valor de Publicado en 2.csv
def update_publicado(row):
    sku = row['SKU']
    if sku in dict_1 and dict_1[sku] == 1 and row['Publicado'] == -1:
        return 1
    return row['Publicado']

# Aplicar la función a df2
df2['Publicado'] = df2.apply(update_publicado, axis=1)

# Guardar el resultado en un nuevo archivo CSV
df2.to_csv('nueva_lista.csv', index=False)

print("Proceso completado. La nueva lista se ha guardado como 'nueva_lista.csv'.")
