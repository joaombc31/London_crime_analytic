# Importação
from google.cloud import bigquery
import pandas as pd
import os
import sys
import re
from pathlib import Path

# Configurações
PROJECT_ID = "curso-ebac-498816"
SOURCE_TABLE = "bigquery-public-data.london_crime.crime_by_lsoa"
TABLE = "curso-ebac-498816.london_crime.crime_five_years"
DATASET_LOCATION = None  
OUTPUT_PATH = (
    r"C:\Users\joaom\OneDrive\Documentos\CURSO EBAC ANALISTA DE DADOS"
    r"\MODULO 38 - MAO NA MASSA BIGQUERY\London_Crime_analytics\data\ready\dados_london_limpos.csv"
)
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Ambiente / Debug
print("=== Ambiente de Execução ===")
print("Python executable:", sys.executable)
print("Python version:", sys.version.splitlines()[0])
print("GOOGLE_APPLICATION_CREDENTIALS:",
      os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
print()

# Cliente BigQuery
client = bigquery.Client(project=PROJECT_ID)

def run_query(query: str):
    """
    Executa uma query no BigQuery respeitando a região do dataset.
    """
    
    if DATASET_LOCATION:
        return client.query(query, location=DATASET_LOCATION)
    return client.query(query)

# Extraçao do dataset bruto (sem limpeza)
print(">>> Extração do BigQuery (RAW)")

sql_raw = f"""
SELECT *
FROM `{TABLE}`
"""
df = run_query(sql_raw).to_dataframe()

print(f"Total de registros RAW: {len(df)}")
print()

# Padronização dos nomes das colunas
print(">>> Padronização dos nomes das colunas")
def normalize_column(col: str) -> str:
    """
    Normaliza o nome das colunas para snake_case.
    """
    col = col.strip().lower()
    col = re.sub(r"[^\w]+", "_", col)  # Remove caracteres especiais
    col = re.sub(r"_+", "_", col)
    return col.strip("_")

df.columns = [normalize_column(c) for c in df.columns]

# Remoção de colunas sem valores (com log)
print(">>> Remoção de colunas totalmente vazias")

cols_before = set(df.columns)

# Remove colunas completamente nulas
df = df.dropna(axis=1, how="all")

cols_after = set(df.columns)

# Identifica colunas removidas
removed_cols = sorted(list(cols_before - cols_after))

print(f"Total de colunas removidas: {len(removed_cols)}")

if removed_cols:
    print("Colunas excluídas:")
    for col in removed_cols:
        print(f" - {col}")
else:
    print("Nenhuma coluna foi removida.")
print()

# Remoção de linhas totalmente vazias
print(">>> Remoção de linhas totalmente vazias")
df = df.dropna(how="all")

# VALIDAÇÕES
print(">>> Validação 1: Volume de registros")

sql_count = f"""
SELECT
    COUNT(*) AS total_registros,
    SUM(total_crimes) AS total_crimes
FROM `{TABLE}`
"""

df_count = run_query(sql_count).to_dataframe()
print(df_count.to_string(index=False))
print()

print(">>> Validação 2: Intervalo temporal")

sql_years = f"""
SELECT
    MIN(year) AS ano_inicial,
    MAX(year) AS ano_final
FROM `{TABLE}`
"""

df_years = run_query(sql_years).to_dataframe()
print(df_years.to_string(index=False))
print()

print(">>> Validação 3: Valores nulos")

sql_nulls = f"""
SELECT
    COUNTIF(year IS NULL) AS anos_nulos,
    COUNTIF(month IS NULL) AS meses_nulos,
    COUNTIF(borough IS NULL) AS borough_nulos,
    COUNTIF(major_category IS NULL) AS major_category_nulos,
    COUNTIF(minor_category IS NULL) AS minor_category_nulos,
    COUNTIF(total_crimes IS NULL) AS total_crimes_nulos
FROM `{TABLE}`
"""

df_nulls = run_query(sql_nulls).to_dataframe()
print(df_nulls.to_string(index=False))
print()

print(">>> Validação 4: Consistência de valores negativos")

sql_negative = f"""
SELECT
    COUNTIF(total_crimes < 0) AS registros_com_total_negativo
FROM `{TABLE}`
"""

df_negative = run_query(sql_negative).to_dataframe()
print(df_negative.to_string(index=False))
print()


# EXTRAÇÃO DA BASE ANALÍTICA PARA POWER BI
print(">>> Extraindo base analítica final para Power BI")

sql_dashboard = f"""
SELECT
    year,
    month,
    borough,
    major_category,
    minor_category,
    total_crimes
FROM `{TABLE}`
ORDER BY year, month, borough, major_category, minor_category
"""

df_dashboard = run_query(sql_dashboard).to_dataframe()

print("Tipos de dados:")
print(df_dashboard.dtypes)
print()

print("Valores nulos por coluna:")
print(df_dashboard.isna().sum())
print()

print("Duplicidades:")
print(df_dashboard.duplicated().sum())
print()

print(f"Linhas finais: {len(df_dashboard)}")
print(f"Colunas finais: {df_dashboard.shape[1]}")
print()

# Salvamento do dataset limpo (Ready)
print(">>> Salvando dataset limpo (READY)")

df.to_csv(OUTPUT_PATH, index=False)

print(f"Arquivo salvo com sucesso :")
print(OUTPUT_PATH)
print(f"Linhas finais: {len(df)}")
print(f"colunas finais: {df.shape[1]}")

# CONSIDERAÇÕES FINAIS
print(">>> Pipeline concluído")
print("- Conexão BigQuery + Python validada")
print("- Tabela analítica Validada no BigQuery")
print("- Dados validados quanto a tipos, nulos e consistência")
print("- Arquivos CSV gerados para Power BI")
print("- Projeto pronto para modelagem e dashboard executivo")