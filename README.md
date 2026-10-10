# 📊 Trabalho de PROB - Analisador Estatístico

<img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white">

<img src="../trabalho-propeest-i/assets/images/tela.png">

> Analisador Estatístico é um projeto desenvolvido para a disciplina de **Probabilidade e Estatística**. O objetivo era construir uma aplicação de linha de comando (CLI) em Python que funcione como um motor de **estatística descritiva**, processando dados digitados no terminal ou lidos de um arquivo `.csv`.

---

## 📍 Intgrantes da Equipe:

**Ana Beatriz Moresi**;\
**Camilla Marchezini**;\
**Catharina de Oliveira**;\
**Filipe Coutinho**;\
**Kauã Fernandes**;\
**Luis Gustavo Bazilio**

## 🚀 Funcionalidades

- **Entrada Flexível:** Dados digitados no terminal (separados por vírgula) ou carregados de um arquivo `.csv`.
- **Parte 1 - Dados Não Agrupados:** Média, Mediana e Moda usando **apenas** o módulo nativo `statistics`.
- **Parte 2 - Dados Agrupados sem Intervalo:** Tabela `xi | fi | Fi` e Média, Mediana e Moda calculadas **a partir da tabela**.
- **Parte 3 - Dados Agrupados com Intervalo:** Classes geradas dinamicamente pela **Fórmula de Sturges**, com Média, Mediana, Moda (Czuber e King), Quartis (Q1, Q3), Decis (D2, D7) e Percentis (P15, P22, P63, P70) por **interpolação**, sem nenhuma biblioteca estatística.
- **Tratamento de Erros:** Arquivo inexistente, extensão errada, pasta no lugar de arquivo, arquivo vazio, textos no meio dos números, cabeçalho no CSV, CSV com `;` e vírgula decimal (padrão do Excel BR).
- **Testes Automatizados:** Testes com `unittest` conferindo as fórmulas contra valores calculados à mão.

---

## 📂 Estrutura do Projeto

```text
TRABALHO-PROPEEST-I/
├── data/
│   └── example.csv           # Base exemplar (120 idades)
├── src/
│   ├── models/               # Moldes das linhas das tabelas (FrequencyRow, ClassInterval)
│   ├── services/             # Regras de negócio (leitura dos dados e as 3 partes do trabalho)
│   │   ├── reader.py         # Leitura do terminal / .csv e validação
│   │   ├── ungrouped.py      # Parte 1 - statistics
│   │   ├── discrete.py       # Parte 2 - tabela sem intervalo
│   │   └── grouped.py        # Parte 3 - tabela com intervalo (Python puro)
│   └── utils/                # Funções utilitárias (menu, exibição dos resultados, limpar terminal)
├── tests/
│   └── test_statistics.py    # Testes automatizados
├── main.py                   # Ponto de entrada do aplicativo
└── README.md                 # Documentação do projeto
```

---

### Formato do CSV

Os números podem estar em uma coluna ou em várias, separados por `,` ou `;`. Se a primeira linha não tiver números, ela é tratada como cabeçalho e ignorada. Quando o separador é `;`, a vírgula é aceita como decimal (`1,75`).

```text
idade
18
22
24
```

---
