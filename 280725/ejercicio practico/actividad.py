import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

possible_paths = [
    CURRENT_DIR,
    os.path.abspath(os.path.join(CURRENT_DIR, "..")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..")),
]

for path in possible_paths:
    if os.path.exists(os.path.join(path, "helper.py")):
        sys.path.append(path)
        break

try:
    import helper as hp
except ImportError:
    raise ImportError("No se pudo encontrar el módulo helper.py en las rutas esperadas.")

plt.style.use('ggplot')
sns.set_theme(font_scale=1.1)

df = pd.read_csv("CAR_DETAILS_FROM_CAR_DEKHO.csv")

"""
 name
 year
 selling_price
 km_driven
 fuel
 seller_type
 transmission
 owner
"""

column_mapping = {
    "name": "Nombre",
    "year": "Año",
    "selling_price": "Precio",
    "km_driven": "Km",
    "fuel": "Combustible",
    "seller_type": "TipoVenta",
    "transmission": "Transmision",
    "owner": "Dueño",
}

df = df.rename(columns=column_mapping)

""" 1. ¿Cuál es el promedio de autos listados por año? Graficá la cantidad de autos por año.
 2. Calculá la media, mediana y moda del `year` (año del vehículo).
 3. Realizá un boxplot del kilometraje recorrido (`km_driven`) para detectar outliers.
 4. Calculá el rango, varianza y desviación estándar del `year`.
 5. Hacé un histograma del `selling_price` para autos que usan combustible "Diesel".
 6. Graficá la distribución de autos por tipo de transmisión (`manual` vs `automatic`).
 7. ¿Cuál es la relación entre el tipo de combustible (`fuel`) y el precio promedio de venta?
 8. Usando un `groupby`, obtené el precio medio por año de fabricación.
 9. Mostrá en un gráfico de barras cuántos autos pertenecen a cada número de dueños (`owner`).
 10. Calculá las medidas de dispersión para el precio de autos automáticos únicamente. 
 """


def ejercicio1():
    data = df["Año"].value_counts().sort_index()
    total_years = data.index.value_counts().sum()
    total_cars = data.values.sum()
    promedio = abs(round(total_cars / total_years))
    
    hp.hbar(data,"Autos listados por año","Cantidad","Año")
    
    print(f"El promedio de autos listados por año es de {promedio} autos")

def ejercicio2():
    año = df["Año"].to_numpy()
    media = hp.get_media(año)
    mediana = hp.get_median(año)
    moda = hp.get_moda(año)

    print(f"Media del año: {media}")
    print(f"Mediana del año: {mediana}")
    print(f"Moda del año: {moda}")


def ejercicio3():
    hp.boxplot(df, x="Año", y="Km", title="Boxplot de Kilometraje por Año")


def ejercicio4():
    rango = hp.get_rank(df, "Año")
    varianza = hp.get_var(df, "Año")
    desv = hp.get_desv(df, "Año")

    print(f"Rango del año: {rango}")
    print(f"Varianza del año: {varianza}")
    print(f"Desviación estándar del año: {desv}")


def ejercicio5():
    condicion = df["Combustible"] == "Diesel"
    hp.histo(df, column="Precio", condition=condicion, title="Precio de autos Diesel")


def ejercicio6():
    data = df["Transmision"].value_counts()
    colores = sns.color_palette("Set2").as_hex()
    hp.pie(data.values, data.index, colores, title="Distribución por Transmisión")


def ejercicio7():
    promedio_por_combustible = df.groupby("Combustible")["Precio"].mean().sort_values()
    hp.vbar(promedio_por_combustible, "Precio promedio por tipo de combustible", "Tipo de Combustible", "Precio Promedio")


def ejercicio8():
    promedio_anual = df.groupby("Año")["Precio"].mean().sort_index()
    hp.hbar(promedio_anual, "Precio promedio por año", "Precio Promedio", "Año")


def ejercicio9():
    data = df["Dueño"].value_counts()
    hp.vbar(data, "Cantidad de autos por tipo de dueño", "Tipo de Dueño", "Cantidad")


def ejercicio10():
    condicion = df["Transmision"].str.lower() == "automatic"
    dispersion = hp.disp(df, column="Precio", condition=condicion)

    print("Medidas de dispersión para autos automáticos:")
    for clave, valor in dispersion.items():
        print(f"{clave}: {valor}")


def main():
    try:
        ejercicio1()
        ejercicio2()
        ejercicio3()
        ejercicio4()
        ejercicio5()
        ejercicio6()
        ejercicio7()
        ejercicio8()
        ejercicio9()
        ejercicio10()
    except Exception as e:
        print(f"Error: {e}")

main()