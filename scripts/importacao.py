# Importação
from google.cloud import bigquery
import pandas as pd
import os
import sys
from pathlib import Path

# Configurações
PROJECT_ID = "curso-ebac-498816"
SOURCE_TABLE = "bigquery-public-data.london_crime.crime_by_lsoa"
TABLE = "curso-ebac-498816.london_crime.crime_five_years"
DATASET_LOCATION = None  

# Ambiente / Debug
print("=== Ambiente de Execução ===")
print("Python executable:", sys.executable)
print("Python version:", sys.version.splitlines()[0])
print("GOOGLE_APPLICATION_CREDENTIALS:",
      os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
print()

# Cliente BigQuery
client = bigquery.Client(project=PROJECT_ID)

def run_query(query: str) -> bigquery.job.QueryJob:
    """
    Executa uma query no BigQuery respeitando a região do dataset.
    """
    
    if DATASET_LOCATION:
        return client.query(query, location=DATASET_LOCATION)
    return client.query(query)


# Query 1 - Preview dos dados

print(">>> Query 1 - Preview (20 linhas)")

sql_preview = f"""
SELECT
   year,
    month,
    borough,
    major_category,
    minor_category,
    total_crimes
FROM `{TABLE}`
ORDER BY year, month, borough, major_category, minor_category
LIMIT 20
"""

df_preview = run_query(sql_preview).to_dataframe()
print(df_preview.to_string(index=False))
print()


# Extraçao do dataset bruto (sem limpeza)
print(">>> Extração do dataset bruto (RAW)")

sql_raw = f"""
SELECT *
FROM `{TABLE}`
"""

df_raw = run_query(sql_raw).to_dataframe()

RAW_OUTPUT_PATH = (
    r"C:\Users\joaom\OneDrive\Documentos\CURSO EBAC ANALISTA DE DADOS"
    r"\MODULO 38 - MAO NA MASSA BIGQUERY\London_Crime_analytics\data\raw\dados_london_crime_raw.csv"
)

os.makedirs(os.path.dirname(RAW_OUTPUT_PATH), exist_ok=True)
df_raw.to_csv(RAW_OUTPUT_PATH, index=False)

print(f"Dataset RAW salvo em:\n{RAW_OUTPUT_PATH}")
print(f"Total de registros RAW: {len(df_raw)}")
print()


# QUERY 2 — EVOLUÇÃO ANUAL DOS CRIMES
print(">>> Query 2: Evolução anual dos crimes")

sql_yearly_trend = f"""
SELECT
    year,
    SUM(total_crimes) AS total_crimes
FROM `{TABLE}`
GROUP BY year
ORDER BY year
"""

df_yearly_trend = run_query(sql_yearly_trend).to_dataframe()

df_yearly_trend["variacao_percentual_ano"] = (
    df_yearly_trend["total_crimes"].pct_change().mul(100).round(2)
)

print(df_yearly_trend.to_string(index=False))
print()


# QUERY 3 — PRIORIDADE POR BAIRRO
print(">>> Query 3: Ranking de bairros prioritários")

sql_borough_priority = f"""
SELECT
    borough,
    SUM(total_crimes) AS total_crimes,
    COUNT(DISTINCT major_category) AS qtd_categorias,
    COUNT(DISTINCT minor_category) AS qtd_subcategorias
FROM `{TABLE}`
GROUP BY borough
ORDER BY total_crimes DESC
"""

df_borough_priority = run_query(sql_borough_priority).to_dataframe()
df_borough_priority["ranking_prioridade"] = (
    df_borough_priority["total_crimes"].rank(method="dense", ascending=False).astype("int64")
)

print(df_borough_priority.to_string(index=False))
print()

# QUERY 4 — TENDÊNCIA POR CATEGORIA DE CRIME
print(">>> Query 4: Tendência por categoria de crime")

sql_category_trend = f"""
WITH base AS (
    SELECT
        major_category,
        year,
        SUM(total_crimes) AS total_crimes
    FROM `{TABLE}`
    GROUP BY major_category, year
),
comparacao AS (
    SELECT
        major_category,
        SUM(CASE WHEN year = 2011 THEN total_crimes ELSE 0 END) AS crimes_2011,
        SUM(CASE WHEN year = 2016 THEN total_crimes ELSE 0 END) AS crimes_2016
    FROM base
    GROUP BY major_category
)
SELECT
    major_category,
    crimes_2011,
    crimes_2016,
    crimes_2016 - crimes_2011 AS variacao_absoluta,
    ROUND(SAFE_DIVIDE(crimes_2016 - crimes_2011, crimes_2011) * 100, 2) AS variacao_percentual
FROM comparacao
ORDER BY variacao_absoluta DESC
"""

df_category_trend = run_query(sql_category_trend).to_dataframe()
print(df_category_trend.to_string(index=False))
print()