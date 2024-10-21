import pandas as pd
import numpy as np  # Importar NumPy para usar la función floor

# Leer el archivo CSV
df = pd.read_csv('productos.csv')

# Filtrar los datos para obtener los productos base (variable)
productos_base = df[df['Tipo'] == 'variable']

# Inicializar una lista para almacenar las filas de variaciones generadas
variaciones_generadas = []

# Iterar sobre cada producto base para generar sus variaciones
for _, producto in productos_base.iterrows():
    # Obtener los valores del atributo y calcular la cantidad de variaciones
    atributos = producto['Valor(es) del atributo 1'].split(',')
    cantidad_variaciones = len(atributos)
    
    # Calcular el inventario promedio para las variaciones y redondear hacia abajo
    inventario_promedio = producto['Inventario'] / cantidad_variaciones
    inventario_promedio_redondeado = np.floor(inventario_promedio)  # Redondear hacia abajo
    
    # Crear una fila de variación para cada atributo
    for atributo in atributos:
        variacion = producto.copy()
        variacion['Tipo'] = 'variation'
        variacion['SKU'] = f"{producto['Nombre']} - {atributo}"
        variacion['Nombre'] = f"{producto['Nombre']} - {atributo}"
        variacion['Inventario'] = inventario_promedio_redondeado  # Asignar el inventario redondeado
        variacion['Cantidad'] = ''  # Dejar vacío si no hay cantidad específica para variaciones
        variacion['Valor(es) del atributo 1'] = atributo
        variacion['Inventario/Cantidad'] = ''  # Dejar vacío ya que no se calcula para variaciones
        variacion['Superior'] = producto['SKU']  # Establecer el SKU del producto base como Superior
        variacion['Categorías'] = ''  # Dejar vacío en variaciones
        variacion['Descripción'] = ''  # Dejar vacío en variaciones
        
        # Agregar la fila de variación a la lista
        variaciones_generadas.append(variacion)

# Convertir la lista de variaciones a un DataFrame
variaciones_df = pd.DataFrame(variaciones_generadas)

# Concatenar productos base con variaciones generadas
resultado = pd.concat([productos_base, variaciones_df], ignore_index=True)

# Guardar el DataFrame procesado a un nuevo archivo CSV
resultado.to_csv('productos_procesados.csv', index=False)

# Mostrar el DataFrame procesado
print(resultado)
