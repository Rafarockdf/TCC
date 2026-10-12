# TCC — Previsão de Cotações de Commodities Agrícolas (Soja e Milho)

Modelo preditivo que integra histórico de cotações, câmbio, clima e indicadores
de safra para prever preços de commodities agrícolas, combinando Prophet
(sazonalidade) e XGBoost (relações não lineares).

## Estrutura de pastas

A estrutura segue os 6 passos definidos no Método Proposto do TCC1.

```
TCC/
├── ColetaBases/            # Passo 1 — Aquisição e Ingestão de Dados
│                           #   notebooks que buscam dados nas fontes externas
│                           #   (yfinance/CBOT-ICE, CEPEA, B3, BCB, INMET, CONAB)
│
├── PreProcessamento/       # Passo 2 — Pré-processamento e Engenharia de Atributos
│                           #   limpeza, tratamento de nulos/outliers, alinhamento
│                           #   de frequências (diário x mensal) e criação de
│                           #   features (lags, médias móveis)
│
├── AnaliseExploratoria/    # Passo 3 — Análise Exploratória (EDA)
│                           #   estatística descritiva, correlações, sazonalidade,
│                           #   decomposição de série temporal
│
├── Modelagem/              # Passo 4 — Treinamento e Otimização dos Modelos
│   └── modelos_treinados/  #   artefatos serializados (Prophet/XGBoost, .pkl/.json)
│
├── Validacao/              # Passo 5 — Validação e Teste
│                           #   Time Series Cross-Validation, cálculo de
│                           #   MAE / RMSE / MAPE, comparação com baselines
│
├── Resultados/             # Passo 6 — Resultados para a monografia
│   └── figuras/            #   gráficos finais, tabelas comparativas, SHAP
│
├── Dados/                  # armazenamento compartilhado entre todas as etapas
│   ├── brutos/              #   dados crus, um subdiretório por fonte
│   │   ├── cotacoes/        #     CBOT/ICE (yfinance), B3, CEPEA
│   │   ├── clima/           #     INMET / NASA POWER
│   │   ├── cambio/          #     Banco Central — USD/BRL
│   │   └── safra/           #     CONAB / USDA
│   ├── processados/         #   bases limpas e alinhadas (parquet/csv)
│   └── tcc.db                #   banco SQLite (gerado pelo pipeline)
│
├── src/                    # código Python reutilizável entre notebooks
│   └── utils/               #   ex: conexão com o SQLite, tema padrão dos gráficos
│
├── venv/                   # ambiente virtual Python
├── requirements.txt
└── README.md
```

## Fluxo de trabalho

`ColetaBases` → `PreProcessamento` → `AnaliseExploratoria` → `Modelagem` →
`Validacao` → `Resultados`

Cada etapa lê da etapa anterior via `Dados/` (arquivos em `Dados/processados/`
ou tabelas em `Dados/tcc.db`) e não deve depender diretamente dos notebooks de
outras pastas — mantém as entregas parciais independentes e fáceis de
reexecutar.
# TCC
