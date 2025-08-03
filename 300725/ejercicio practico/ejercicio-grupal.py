import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = "2.Car_Price_Prediction.csv"

df = pd.read_csv(file)

"""
1. Hacer un filtrado de transmiciones automaticos y manuales.
2. Graficar el % de transmiciones automaticos y manuales.
3. Buscar un moda, mediana y media del precio.
4. Cacular el minimo y maximo de precios.
5. Calcular Q1, Q3 de precios y graficar
"""

# 1.

count = df["Transmission"].value_counts()
automatic = count.get("Automatic",0)
manual = count.get("Manual",0)


# 2.
valores = [automatic,manual]
etiquetas = ['Automatico', 'Manual']
colores = ["#3be6afd6", "#924526D6"]

plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', colors=colores, startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 0.8})
plt.title("Proporción de vehiculos con transmicion automatica y manual")
plt.axis('equal')
plt.tight_layout()
plt.show()


# 3.

price = pd.to_numeric(df['Price'], errors='coerce')

Media = np.nanmean(price)
Moda = price.mode()[0]
Median = price.median()

# poner 5 decimales maximo --> price.median().__round__(ndigits=5)


# 4.

precio_maximo = price.max()
precio_minimo = price.min()


# 5.

Q = price.quantile(0.25, 0.75)
Q1 = Q[0]
Q3 = Q[1]