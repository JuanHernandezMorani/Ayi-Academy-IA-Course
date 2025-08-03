import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union, List

def help(type: str):
    functions = {
        "hbar": """ hbar(data, title, xlabel, ylabel) 
    Crea y muestra un gráfico de barras horizontales. Ideal para rankings o comparaciones visuales.
    - data: pandas.Series con los valores a graficar.
    - title: Título del gráfico (str).
    - xlabel/ylabel: Etiquetas de los ejes X e Y (str).
    """,
        "vbar": """ vbar(data, title, xlabel, ylabel) 
    Crea y muestra un gráfico de barras verticales.
    - data: pandas.Series con los valores a graficar.
    - title: Título del gráfico (str).
    - xlabel/ylabel: Etiquetas de los ejes X e Y (str).
    """,
        "pie": """ pie(valores, etiquetas, colores, title)
    Crea y muestra un gráfico de torta porcentual.
    - valores: array-like con los valores numéricos.
    - etiquetas: array-like con los nombres de cada categoría.
    - colores: lista de colores (RGB o RGBA en hex, ej: "#FFAA00").
    - title: Título del gráfico (str).
    Si hay muchas categorías, las etiquetas se muestran como leyenda.
    """,
        "normalize": """ normalize(data)
    Normaliza un array de valores numéricos entre 0 y 1 usando min-max scaling.
    - data: numpy.ndarray.
    Retorna: nuevo array normalizado (numpy.ndarray).
    """,
        "get_moda": """ get_moda(data, with_repetition=False)
    Calcula la moda (valor que más se repite).
    - data: numpy.ndarray.
    - with_repetition (bool): Si es True, devuelve una lista con [valor, cantidad de repeticiones].
      Si es False (default), solo devuelve el valor.
    Ignora NaN por defecto.
    """,
        "get_media": """ get_media(data, nan=False)
    Calcula la media (promedio) de un array.
    - data: numpy.ndarray.
    - nan (bool): Si es True, usa np.nanmean para ignorar NaN. Default: False.
    Retorna: valor float con la media.
    """,
        "get_median": """ get_median(data, nan=False)
    Calcula la mediana de un array.
    - data: numpy.ndarray.
    - nan (bool): Si es True, usa np.nanmedian para ignorar NaN. Default: False.
    Retorna: valor float con la mediana.
    """,
        "boxplot": """ boxplot(df, x, y, hue=None, title="")
    Crea un gráfico de caja para explorar la distribución de una variable numérica (y) por categorías (x).
    - df: DataFrame.
    - x: variable categórica.
    - y: variable numérica.
    - hue: (opcional) para separar por subcategoría.
    - title: Título del gráfico.
    """,
        "get_rank": """ get_rank(df, column)
    Calcula el rango (máximo - mínimo) de una columna numérica.
    - df: DataFrame.
    - column: Nombre de la columna.
    """,
        "get_var": """ get_var(df, column)
    Calcula la varianza de una columna numérica.
    - df: DataFrame.
    - column: Nombre de la columna.
    """,
        "get_desv": """ get_desv(df, column)
    Calcula la desviación estándar de una columna numérica.
    - df: DataFrame.
    - column: Nombre de la columna.
    """,
        "histo": """ histo(df, column, condition=None, bins=20, title="")
    Genera un histograma de una columna numérica.
    - df: DataFrame.
    - column: Columna numérica a graficar.
    - condition: (opcional) filtro para aplicar antes.
    - bins: cantidad de bins (por defecto 20).
    - title: título del gráfico.
    """,
        "disp": """ disp(df, column, condition=None)
    Calcula medidas de dispersión: rango, varianza y desviación estándar.
    - df: DataFrame.
    - column: Columna numérica.
    - condition: (opcional) filtro booleano para aplicar.
    Retorna un dict con las 3 medidas.
    """,
    }

    if not isinstance(type, str):
        return print("El dato ingresado no es del tipo string")

    type = type.lower()

    if type == "all":
        for name, doc in functions.items():
            print(f"\n{name.upper()}:\n{doc}")
    elif type in functions:
        print(functions[type])
    else:
        print(
            f'helper no contiene ninguna función con el nombre "{type}", los valores permitidos son: all, {", ".join(functions.keys())}'
        )

def format_number(value: float, use_decimals: bool = True, decimals: int = 2, percent: bool = False) -> str:
    if percent:
        value *= 100

    if use_decimals:
        formatted = f"{value:,.{decimals}f}"
    else:
        formatted = f"{int(round(value)):,}"

    # Se reemplaza ',' por '.' y '.' por ',' como se usa en Argentina
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    
    if percent:
        formatted += "%"

    return formatted

def hbar(data: pd.Series, title: str, xlabel: str, ylabel: str):
    plt.figure(figsize=(12, 8))

    y_pos = range(len(data))
    bars = plt.barh(y_pos, data.values, color="skyblue")

    plt.yticks(ticks=y_pos, labels=data.index)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis="x", alpha=0.3)

    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(
        width + 2,
        bar.get_y() + bar.get_height() / 2,
        format_number(width, use_decimals=False),
        va="center",
    )

    plt.tight_layout()
    plt.show()

def vbar(data: pd.DataFrame, title: str, xlabel: str, ylabel: str):
    plt.figure(figsize=(12, 8))
    bars = plt.bar(data.index, data.values, color="skyblue")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        x = bar.get_x() + bar.get_width() / 2
        plt.text(
            x, height + (height * 0.02),
            format_number(height, use_decimals=False),
            ha="center", va="bottom"
        )

    plt.tight_layout()
    plt.show()

def pie(valores, etiquetas, colores, title: str, decimales: int = 1):
    fig, ax = plt.subplots()

    use_labels = len(etiquetas) <= 10
    labels = etiquetas if use_labels else None

    def format_pct(pct):
        return format_number(pct / 100, use_decimals=True, decimals=decimales, percent=True)

    wedges, texts, autotexts = ax.pie(
        valores,
        labels=labels,
        autopct=format_pct,
        colors=colores,
        startangle=90,
        wedgeprops={"edgecolor": "black", "linewidth": 0.8},
        textprops={"fontsize": 8},
    )

    if not use_labels:
        ax.legend(
            wedges,
            etiquetas,
            title="Categorías",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=8,
            title_fontsize=9,
        )

    ax.set_title(title)
    ax.axis("equal")
    plt.tight_layout()
    plt.show()

def normalize(data: np.ndarray):
    return (data - data.min()) / (data.max() - data.min())

def get_moda(
    data: np.ndarray, with_repetition: bool = False
) -> Union[float, List[Union[float, int]]]:
    data_no_nan = data[~np.isnan(data)]

    valores, conteos = np.unique(data_no_nan, return_counts=True)

    if len(conteos) == 0:
        return np.nan if not with_repetition else [np.nan, 0]

    index_moda = np.argmax(conteos)

    if with_repetition:
        return [format_number(valores[index_moda]), format_number(conteos[index_moda])]
    else:
        return format_number(valores[index_moda])

def get_media(data: np.ndarray, nan: bool = False) -> float:
    return format_number(np.nanmean(data) if nan else np.mean(data))

def get_median(data: np.ndarray, nan: bool = False) -> float:
    return format_number(np.nanmedian(data) if nan else np.median(data))

def boxplot(df: pd.DataFrame, x: str, y: str, hue: str = None, title: str = ""):
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x=x, y=y, hue=hue)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    if hue:
        plt.legend(title=hue)
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.show()

def get_rank(df: pd.DataFrame, column: str) -> float:
    return format_number(np.nanmax(df[column]) - np.nanmin(df[column]))

def get_var(df: pd.DataFrame, column: str) -> float:
    return format_number(np.nanvar(df[column]))

def get_desv(df: pd.DataFrame, column: str) -> float:
    return format_number(np.nanstd(df[column]))

def histo(
    df: pd.DataFrame,
    column: str,
    condition: pd.Series = None,
    bins: int = 20,
    title: str = "",
):
    if condition is not None:
        df = df[condition]

    plt.figure(figsize=(10, 6))
    plt.hist(
        df[column].dropna(), bins=bins, color="skyblue", edgecolor="black", alpha=0.7
    )
    plt.title(title or f"Histograma de {column}")
    plt.xlabel(column)
    plt.ylabel("Frecuencia")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def disp(df: pd.DataFrame, column: str, condition: pd.Series = None) -> dict:
    if condition is not None:
        df = df[condition]

    return {
        "rango": get_rank(df, column),
        "varianza": get_var(df, column),
        "desviacion estandar": get_desv(df, column),
    }