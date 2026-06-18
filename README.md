# London Crime Analytics

## 📊 Análise da Criminalidade em Londres (2011–2016)

Projeto desenvolvido utilizando **Google BigQuery**, **Python** e **Power BI**, com o objetivo de transformar dados brutos de criminalidade em informações analíticas que apoiem a tomada de decisão em segurança pública.

---

## 🎯 Objetivo

Responder à seguinte pergunta de negócio:

> Quais tipos de crime estão crescendo ou diminuindo ao longo do tempo em Londres, em quais bairros e onde devem ser priorizadas ações de prevenção e alocação de recursos policiais?

---

## 🛠 Tecnologias Utilizadas

- Google BigQuery
- Python 3.12
- Pandas
- Google Cloud SDK
- Power BI Desktop
- Visual Studio Code
- Git e GitHub

---

## 📂 Estrutura do Projeto

```text
LONDON_CRIME_ANALYTICS
│
├── data
│   ├── raw
│   └── ready
│
├── dash
│   └── london_crime_dashboard.pbix
│
├── prints
│   ├── print_01_Consulta_realizada.png
│   ├── print_02_schema_tabela_salva.png
│   └── print_03_preview_dados.png
│   └── Todas as prints de consultas│
│
├── scripts
│   ├── importacao.py
│   └── limpeza_padronizacao.py
│
└── README.md
```

---

## 🗄 Fonte dos Dados

Base pública do Google BigQuery:

```sql
bigquery-public-data.london_crime.crime_by_lsoa
```

Para otimizar o processamento e reduzir custos de consulta, foi criada uma tabela analítica dentro do projeto:

```sql
curso-ebac-498816.london_crime.crime_five_years
```

A tabela foi filtrada para o período:

```text
2011 a 2016
```

e agregada para utilização em análises e dashboards.

---

## 🔄 Pipeline Desenvolvido

### 1. Estruturação dos Dados

- Criação do dataset `london_crime`
- Criação da tabela analítica `crime_five_years`
- Validação do schema
- Verificação dos tipos de dados
- Verificação do volume de registros

### 2. Integração Python + BigQuery

- Autenticação no Google Cloud
- Conexão programática ao BigQuery
- Execução de consultas SQL
- Extração dos dados para DataFrames Pandas

### 3. Tratamento e Validação

- Padronização dos nomes das colunas
- Validação de tipos de dados
- Verificação de valores nulos
- Verificação de valores negativos
- Verificação de registros duplicados
- Exportação da base final tratada

### 4. Power BI

Criação de dashboard executivo contendo:

- Total de Crimes
- Total de Bairros
- Total de Categorias
- Top 10 Bairros com Maior Número de Crimes
- Categorias Criminais com Maior Incidência
- Evolução Total da Criminalidade
- Tendência dos Crimes por Categoria
- Análise de Bairros Prioritários

---

## 📈 Principais Indicadores

- Total de Crimes
- Total de Bairros Analisados
- Total de Categorias Criminais
- Evolução Anual da Criminalidade
- Distribuição de Crimes por Bairro
- Distribuição de Crimes por Categoria

---

## 📷 Evidências

O projeto contém registros da implementação:

- Estrutura da tabela no BigQuery
- Schema da tabela analítica
- Preview dos dados carregados
- Dashboard final desenvolvido no Power BI

---

## 📋 Resultados

A análise permitiu identificar:

- Os bairros com maior concentração de crimes.
- As categorias criminais mais recorrentes.
- A evolução da criminalidade ao longo dos anos.
- Áreas prioritárias para alocação de recursos policiais.
- Tendências de crescimento e redução dos principais tipos de crime.

---

## 👨‍💻 Autor

**João Euzébio**

Projeto desenvolvido como atividade prática do curso de **Analista de Dados – EBAC**.