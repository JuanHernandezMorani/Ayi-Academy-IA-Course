import numpy as np
import pandas as pd

df = pd.read_csv("market.csv")

pesos = df["Item_Weight"].to_numpy()
ventas = df["Item_Outlet_Sales"].to_numpy()
precios = df["Item_MRP"].to_numpy()
visibilidad = df["Item_Visibility"].to_numpy()


# Ejercicio 1

#np.mean(arg) != np.nanmean(arg)
media_pesos = np.nanmean(pesos)

# Ejercicio 2

valores, conteos = np.unique(pesos[~np.isnan(pesos)], return_counts=True)
index_moda = np.argmax(conteos)

repeticion = conteos[index_moda]
moda = valores[index_moda]

# Ejercicio 3
filtrado = df[(precios > 250)&(visibilidad < 0.02)]

# Ejercicio 4

mask = ~np.isnan(precios) & ~np.isnan(ventas)
p_500 = precios[mask][:500]
v_500 = ventas[mask][:500]
arr_dif = np.abs(p_500 - v_500)

# Ejercicio 5

visibilidad_normalizada = (visibilidad - visibilidad.min()) / (visibilidad.max() - visibilidad.min())

# Ejercicio 6

matris = np.column_stack((pesos, precios, ventas))

m_media_col1 = np.nanmean(matris[:, 0])
m_media_col2 = np.nanmean(matris[:, 1])
m_media_col3 = np.nanmean(matris[:, 2])


# Ejercicio 7

valores, conteos = np.unique(pesos[np.isnan(pesos)], return_counts=True)
index_moda = np.argmax(conteos)

repeticion = conteos[index_moda]
prod_nan = df[np.isnan(df["Item_Weight"])]


# Ejercicio 8

precio_imaginario = np.abs(np.random.normal(loc=200, scale=30, size=100))


# Ejercicio 9

mask = ~np.isnan(precios) & ~np.isnan(ventas)
p_clean = precios[mask]
v_clean = ventas[mask]
relacion = np.corrcoef([p_clean,v_clean])


# Ejercicio 10

round_arr = np.round(pesos[~np.isnan(pesos)],2)