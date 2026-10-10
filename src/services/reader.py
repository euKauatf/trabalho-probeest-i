# src/services/reader.py

import csv # Importando csv (nativo do Python) pra ler o arquivo
import math # Importando math só pra checar se o número é finito (nada de "nan" ou "inf")
import os # Importando os pra checar se o caminho é uma pasta


# Erro próprio pra quando os dados não servem pra análise (arquivo vazio, sem números, etc.)
class DataError(Exception):
    pass


# -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Função que converte texto em número ->
# <- <- <- <- <- <- <-  <- <- <- <- <- <-
def parse_number(text: str):
    number = float(text.strip().replace(",", ".")) # Aceita "24.5" e "24,5"

    if (not math.isfinite(number)):
        raise ValueError(f"Valor não finito: {text}")

    return number


# -> -> -> -> -> -> -> -> ->  -> -> -> -> -> -> -> ->
# <- Função que separa o que é número do que é lixo ->
# <- <- <- <- <- <- <- <- <-  <- <- <- <- <- <- <- <-
def parse_tokens(tokens: list):
    values = []
    invalid = []

    for token in tokens:
        token = token.strip()
        if (token == ""): # Célula vazia a gente só ignora
            continue

        try:
            values.append(parse_number(token))
        except ValueError:
            invalid.append(token) # Guardando os inválidos pra avisar o usuário depois

    return values, invalid


# -> -> -> -> -> -> -> -> -> ->  -> -> -> ->
# <- Função que lê os dados do terminal ->
# <- <- <- <- <- <- <- <- <- <-  <- <- <- <-
def read_terminal(raw: str):
    values, invalid = parse_tokens(raw.split(","))

    if (len(values) == 0):
        raise DataError("Nenhum número válido foi digitado.")

    return values, invalid


# -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Função que lê o conteúdo do arquivo ->
# <- <- <- <- <- <- <-  <- <- <- <- <- <-
def read_file_content(path: str):
    # Primeiro tenta UTF-8 (com ou sem BOM), se não der tenta latin-1 (CSV salvo pelo Excel em PT-BR)
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as file:
            return file.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1", newline="") as file:
            return file.read()


# -> -> -> -> -> -> ->  -> -> -> -> ->
# <- Função que lê os dados do .csv ->
# <- <- <- <- <- <- <-  <- <- <- <- <-
def read_csv(path: str):
    if (not path.lower().endswith(".csv")):
        raise DataError("O arquivo precisa ter a extensão .csv")

    if (os.path.isdir(path)): # No Windows abrir pasta dá PermissionError, então a gente avisa antes
        raise IsADirectoryError(path)

    content = read_file_content(path) # FileNotFoundError e PermissionError sobem pra interface tratar

    # Se tiver ";" no arquivo, ele é o separador (padrão do Excel BR, onde a vírgula é decimal)
    delimiter = ";" if (";" in content) else ","
    rows = [row for row in csv.reader(content.splitlines(), delimiter=delimiter) if row]

    if (len(rows) == 0):
        raise DataError("O arquivo está vazio.")

    # Se a primeira linha não tiver nenhum número, é cabeçalho (tipo "idade") e a gente pula
    header = None
    first_values, _ = parse_tokens(rows[0])
    if (len(first_values) == 0):
        header = rows.pop(0)

    tokens = []
    for row in rows:
        tokens.extend(row)

    values, invalid = parse_tokens(tokens)

    if (len(values) == 0):
        raise DataError("O arquivo não possui nenhum número válido.")

    return values, invalid, header
