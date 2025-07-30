import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime as dt

df = pd.read_csv("aac_shelter_cat_outcome_eng.csv")

df = df.drop(columns=["Unnamed: 0"], errors="ignore")

df = df.rename(columns={
    "animal_id": "ID",
    "name": "Nombre",
    "date_of_birth": "FechaNacimiento",
    "outcome_type": "TipoResultado",
    "outcome_subtype": "SubtipoResultado",
    "animal_type": "TipoAnimal",
    "sex_upon_outcome": "Sexo",
    "age_upon_outcome": "Edad",
    "breed": "Raza",
    "color": "Color"
})


# Ejercicio 1

cantidad_gatos = (df['TipoAnimal'] == 'Cat').sum()
column_labels = ["Tipo de Animal", "Cantidad"]
table_data = [["Gatos (Cat)", cantidad_gatos]]

fig, ax = plt.subplots()
ax.axis('off')

tabla = ax.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='top')
tabla.auto_set_font_size(False)
tabla.set_fontsize(12)
tabla.scale(1.5, 1.5)

plt.tight_layout()
plt.show()


# Como solo tenia Cat -> print(f"Cantidad total de gatos: {len(df)}")

# Ejercicio 2

df['Raza'].value_counts().head(5).plot(kind='bar', color='green')
plt.title("Top 5 razas más comunes")
plt.ylabel("Cantidad")
plt.xlabel("Raza")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.45,color='grey')
plt.tight_layout()
plt.show()

# Ejercicio 3

sin = df['Nombre'].isna().sum()
con = df['Nombre'].notna().sum()

valores = [con, sin]
etiquetas = ['Con nombre', 'Sin nombre']
colores = ["#3be6afd6", "#924526D6"]

plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', colors=colores, startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 0.8})
plt.title("Proporción de animales con y sin nombre")
plt.axis('equal')
plt.tight_layout()
plt.show()

# Ejercicio 4

valor = df[df['TipoResultado'] == 'Adoption'].groupby('Raza').size().sort_values(ascending=False).head(10).iloc[::-1]
etiquetas = ['Cantidad', 'Raza']

plt.figure(figsize=(10, 6))
bars = plt.barh(valor.index, valor.values, color="skyblue")

plt.title("Frecuencia de adopcion de las razas mas comunes")
plt.ylabel("Raza")
plt.xlabel("Cantidad")
plt.grid(axis="x", alpha=0.45,color='grey')

for bar in bars:
    width = bar.get_width()
    plt.text(
        (width + 0.5), bar.get_y() + bar.get_height() / 2, f"{int(width)}", va="center"
    )

plt.tight_layout()
plt.show()


# Ejercicio 5

data = df[df['TipoResultado'] == 'Adoption'].groupby('Edad').size().sort_values(ascending=False).head(1)
column_labels = ["Edad", "Cantidad"]
table_data = [[data.index[0], data.values[0]]]

fig, ax = plt.subplots()
ax.axis('off')

tabla = ax.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='top')
tabla.auto_set_font_size(False)
tabla.set_fontsize(12)
tabla.scale(1.5, 1.5)

plt.tight_layout()
plt.show()


# Ejercicio 6


df_nombres = df.groupby('Nombre').size().sort_values(ascending=False)
top10 = df_nombres.head(10).iloc[::-1]
etiquetas = ['Cantidad', 'Nombre']

plt.figure(figsize=(10, 6))
bars = plt.barh(top10.index, top10.values, color="skyblue")

plt.title("Top 10 nombres más comunes")
plt.ylabel("Nombre")
plt.xlabel("Cantidad")
plt.grid(axis="x", alpha=0.45,color='grey')

for bar in bars:
    width = bar.get_width()
    plt.text(
        (width + 0.5), bar.get_y() + bar.get_height() / 2, f"{int(width)}", va="center"
    )

plt.tight_layout()
plt.show()


# Ejercicio 7


conditions =  [
    (df['Raza'] == 'domestic shorthair') | (df['Raza'] == 'domestic mediumhair') | (df['Raza'] == 'domestic longhair')
]

results = [True]

df["Cruza"] = np.select(conditions, results, default=False)


# Ejercicio 8

df['FechaNacimiento'] = pd.to_datetime(df['FechaNacimiento'], errors='coerce') # errors fuerza a nulos para evitar crasheo
df['AñoNacimiento'] = df['FechaNacimiento'].dt.year
df['FueAdoptado'] = df['TipoResultado'] == 'Adoption'
adopciones_por_año = df.groupby('AñoNacimiento')['FueAdoptado'].mean()
adopciones_por_año_pct = adopciones_por_año * 100

adopciones_por_año_pct.plot(kind='line', marker='o', color='darkorange')
plt.title('Tasa de adopción según año de nacimiento')
plt.xlabel('Año de nacimiento')
plt.ylabel('Porcentaje de probabilidad de adopción')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# Ejercicio 9


def edad_a_dias(edad):
    if pd.isna(edad):
        return np.nan
    edad = str(edad).lower()
    if 'year' in edad:
        return int(edad.split()[0]) * 365
    elif 'month' in edad:
        return int(edad.split()[0]) * 30
    elif 'week' in edad:
        return int(edad.split()[0]) * 7
    elif 'day' in edad:
        return int(edad.split()[0])
    else:
        return np.nan
    
df['EdadEnDias'] = df['Edad'].apply(edad_a_dias)

tabla_edad_resultado = df.groupby(['Edad', 'TipoResultado']).size().unstack(fill_value=0)
tabla_edad_resultado['EdadEnDias'] = tabla_edad_resultado.index.to_series().apply(edad_a_dias)
tabla_ordenada = tabla_edad_resultado.sort_values('EdadEnDias', ascending=False).drop(columns='EdadEnDias')

plt.figure(figsize=(10, 8))
sns.heatmap(tabla_ordenada.iloc[::-1], cmap="YlGnBu", annot=True, fmt="d", annot_kws={"size": 7}, linewidths=0.1)
plt.title("Distribución de resultados según la edad")
plt.xlabel("Tipo de resultado")
plt.ylabel("Edad del animal")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Ejercicio 10

df[df['TipoResultado'] == 'Adoption'].to_csv('adoptados.csv', index=False)