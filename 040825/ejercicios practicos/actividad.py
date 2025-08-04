import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

sns.set_theme(style="whitegrid")
df = pd.read_csv("customer.csv")

plt.figure(figsize=(10, 5))
sns.boxplot(x='Coverage', y='ClaimAmount', data=df)
plt.title("Distribución de ClaimAmount según tipo de Coverage")
plt.show()

plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de correlación entre variables numéricas")
plt.show()

plt.figure(figsize=(10, 5))
sns.violinplot(x='VehicleSize', y='CustomerLifetimeValue', data=df)
plt.title("Distribución del valor del cliente según el tamaño del vehículo")
plt.show()

df['EffectiveToDate'] = pd.to_datetime(df['EffectiveToDate'])
df_sorted = df.sort_values("EffectiveToDate")

plt.figure(figsize=(12, 5))
sns.lineplot(data=df_sorted, x='EffectiveToDate', y='ClaimAmount', ci=None)
plt.title("Evolución temporal de ClaimAmount")
plt.xticks(rotation=45)
plt.show()

g = sns.FacetGrid(df, col="VehicleSize", row="Coverage", margin_titles=True, height=3)
g.map_dataframe(sns.boxplot, x="Gender", y="ClaimAmount")
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Variación de ClaimAmount según género, cobertura y tamaño de vehículo")
plt.show()

sns.pairplot(df[['CustomerLifetimeValue', 'Income', 'MonthlyPremiumAuto', 'ClaimAmount']])
plt.suptitle("Relaciones entre métricas financieras", y=1.02)
plt.show()

sample = df['ClaimAmount'].dropna()
media = sample.mean()
std = sample.std()
n = len(sample)
conf_int = stats.norm.interval(0.95, loc=media, scale=std/np.sqrt(n))
print(f"Intervalo de confianza del 95% para ClaimAmount: {conf_int}")

basic = df[df['Coverage'] == 'Basic']['ClaimAmount']
premium = df[df['Coverage'] == 'Premium']['ClaimAmount']

t_stat, p_val = stats.ttest_ind(basic, premium, equal_var=False)
print(f"T-statistic: {t_stat}, p-value: {p_val}")