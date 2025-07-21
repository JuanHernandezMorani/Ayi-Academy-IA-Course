import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

file = "air-quality-monitoring-sites-summary.csv"

# Configuración básica para gráficos más bonitos
plt.style.use("default")
plt.rcParams["figure.figsize"] = (10, 6)

df = pd.read_csv(file)

df = df.dropna(axis=1, how="all")

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

column_mapping = {
    "NSW air quality monitoring (AQMN) site": "Site",
    "AQMN Region": "Region",
    "Sub-region,where applicable": "Subregion",
    "Site address": "Address",
    "Latitude\n(South)": "Latitude",
    "Longitude\n(East)": "Longitude",
    "Altitude (ahd)": "Altitude",
    "Commissioned": "Commissioned",
    "Status": "Status",
}

df = df.rename(columns=column_mapping)

main_cols = ["Site", "Region", "Address", "Latitude", "Longitude", "Status"]

df.isna().sum()

df = df.dropna(subset=["Latitude", "Longitude", "Site"])


def convert_dms_to_decimal(dms_string):

    if pd.isna(dms_string) or dms_string == "":
        return None

    try:
        numbers = re.findall(r"\d+(?:\.\d+)?", str(dms_string))

        if len(numbers) >= 2:
            degrees = float(numbers[0])
            minutes = float(numbers[1])
            seconds = float(numbers[2]) if len(numbers) > 2 else 0

            decimal = degrees + minutes / 60 + seconds / 3600

            if "South" in str(dms_string) or decimal > 0:
                decimal = -abs(decimal)

            return decimal
    except:
        pass

    return None


df["Latitude"] = df["Latitude"].apply(convert_dms_to_decimal)
df["Longitude"] = df["Longitude"].apply(convert_dms_to_decimal)

df_geo = df.dropna(subset=["Latitude", "Longitude", "Site"]).copy()

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
altitude_data = df_geo["Altitude"].dropna()
plt.hist(altitude_data, bins=15, color="lightblue", edgecolor="black", alpha=0.7)
plt.title("Distribución de Altitudes")
plt.xlabel("Altura (metros)")
plt.ylabel("Cantidad de estaciones")
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)

plt.boxplot(
    altitude_data,
    vert=True,
    patch_artist=True,
    boxprops=dict(facecolor="lightgreen", alpha=0.7),
)
plt.ylabel("Altura (metros)")
plt.title("Estadísticas de Altitud")
plt.grid(True, alpha=0.3)

plt.tight_layout()



plt.figure(figsize=(12, 8))

plt.scatter(
    df_geo["Longitude"],
    df_geo["Latitude"],
    c="red",
    alpha=0.6,
    s=50,
    edgecolors="black",
    linewidth=0.5,
)

plt.title("Ubicaciones de Estaciones de Monitoreo en NSW, Australia")
plt.xlabel("Longitud (Este)")
plt.ylabel("Latitud (Sur)")
plt.grid(True, alpha=0.3)

plt.text(
    0.02,
    0.98,
    f"Total: {len(df_geo)} estaciones",
    transform=plt.gca().transAxes,
    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
    verticalalignment="top",
)

lat_range = df_geo["Latitude"].max() - df_geo["Latitude"].min()
lon_range = df_geo["Longitude"].max() - df_geo["Longitude"].min()
plt.xlim(
    df_geo["Longitude"].min() - lon_range * 0.1,
    df_geo["Longitude"].max() + lon_range * 0.1,
)
plt.ylim(
    df_geo["Latitude"].min() - lat_range * 0.1,
    df_geo["Latitude"].max() + lat_range * 0.1,
)

plt.tight_layout()


cols_contaminantes = ["PM10", "PM2.5", "NO/NO2/NOx", "SO2", "O3", "CO"]
available_pollutants = [col for col in cols_contaminantes if col in df_geo.columns]

if available_pollutants:
    pollutant_counts = (
        df_geo[available_pollutants].notna().sum().sort_values(ascending=True)
    )

    plt.figure(figsize=(10, 6))
    bars = plt.barh(
        range(len(pollutant_counts)), pollutant_counts.values, color="coral", alpha=0.7
    )
    plt.yticks(range(len(pollutant_counts)), pollutant_counts.index)
    plt.xlabel("Número de estaciones")
    plt.title("Estaciones que Miden Cada Contaminante")
    plt.grid(True, alpha=0.3, axis="x")

    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(
            width + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}",
            ha="left",
            va="center",
        )

    plt.tight_layout()

    

    # ejercicio 1

    station_max = df.loc[df["Altitude"].idxmax()]
    station_min = df.loc[df["Altitude"].idxmin()]
    nombres = [station_min["Site"], station_max["Site"]]
    alturas = [station_min["Altitude"], station_max["Altitude"]]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(nombres, alturas, color=["red", "green"], alpha=0.4)

    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 5,
            f"{height:.1f} m",
            ha="center",
            va="bottom",
            fontsize=12,
        )

    print(f"La estación más alta es '{station_max['Site']}' con {station_max['Altitude']} metros.")
    print(f"La estación más baja es '{station_min['Site']}' con {station_min['Altitude']} metros.")

    plt.title("Estaciones con Altura Máxima y Mínima")
    plt.ylabel("Altura (metros)")
    plt.grid(axis="x", alpha=0.45)
    plt.subplots_adjust(top=0.85, bottom=0.2, left=0.1, right=0.95)
    

    # ejercicio 2

    df_pollution_alt = pd.DataFrame()

    for pollutant in available_pollutants:
        df_temp = df[["Altitude", pollutant]].copy()
        df_temp["Contaminante"] = pollutant
        df_temp["SeMide"] = df_temp[pollutant].notna()
        df_pollution_alt = pd.concat(
            [df_pollution_alt, df_temp[["Altitude", "Contaminante", "SeMide"]]],
            ignore_index=True,
        )


    print("""Observación:
Este gráfico muestra cómo varía la altitud según si una estación mide o no un contaminante.
Si los boxplots tienen diferencias notorias de altura entre 'Se mide = True' y 'False', puede haber relación.
Caso contrario, la altitud no influye significativamente en qué contaminantes se miden.""")
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Contaminante", y="Altitude", hue="SeMide", data=df_pollution_alt)
    plt.title("Relación entre Altitud y Presencia de Monitoreo por Contaminante")
    plt.ylabel("Altitud (m)")
    plt.xlabel("Contaminante")
    plt.legend(title="¿Se mide?")
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    

    # ejercicio 3

    region_counts = df["Region"].value_counts().sort_values()

    plt.figure(figsize=(10, 6))
    bars = plt.barh(region_counts.index, region_counts.values, color="skyblue")

    plt.title("Cantidad de Estaciones por Región")
    plt.xlabel("Número de estaciones")
    plt.ylabel("Región")
    plt.grid(axis="x", alpha=0.3)

    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 0.5, bar.get_y() + bar.get_height() / 2, f"{int(width)}", va="center"
        )

    plt.tight_layout()
    
    
    # ejercicio 4
    
    plt.figure(figsize=(12, 8))

    scatter = plt.scatter(
        df['Longitude'], df['Latitude'],
        c=df['Altitude'], cmap='viridis',
        s=60, edgecolors='black', alpha=0.7
    )

    plt.colorbar(scatter, label='Altitud (m)')
    plt.title("Mapa de Estaciones Coloreado por Altitud")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()