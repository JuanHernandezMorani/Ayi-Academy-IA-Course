import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore, skew, kurtosis
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

possible_paths = [
    CURRENT_DIR,
    os.path.abspath(os.path.join(CURRENT_DIR, "..")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..")),
]

for path in possible_paths:
    if os.path.exists(os.path.join(path, "helper.py")):
        sys.path.append(path)
        break

try:
    import helper as hp
except ImportError:
    raise ImportError(
        "No se pudo encontrar el módulo helper.py en las rutas esperadas."
    )

"""
1. ¿Cuál es el tipo de distribución que presenta `ClaimAmount`?
2. Identificá si hay outliers en `CustomerLifetimeValue` usando visualización.
3. Usá el método del IQR para detectar outliers en `MonthlyPremiumAuto`.
4. Usá el método del Z-score en `TotalClaimAmount` y reportá cuántos outliers hay.
5. Compará `ClaimAmount` según `Education` con un boxplot.
6. ¿Qué diferencias ves entre `VehicleSize` y `CustomerLifetimeValue`?
7. Calculá y analizá la asimetría de `MonthlyPremiumAuto`.
8. ¿Qué indica la curtosis de `TotalClaimAmount`?
9. Usá un `pairplot` con variables numéricas del dataset.
10. ¿Cómo puede afectar la presencia de outliers en un modelo predictivo?
"""
