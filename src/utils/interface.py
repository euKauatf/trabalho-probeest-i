# src/utils/interface.py

import csv # Só pra pegar o csv.Error (arquivo malformado)
import os

from src.services.reader import read_terminal, read_csv, DataError
from src.utils.report import show_report
from src.utils.terminal import clear

# Caminho do CSV de exemplo (funciona de qualquer pasta que rodar o main.py)
EXAMPLE_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "example.csv")


# Avisa quais valores foram ignorados por não serem números (mostra só os 5 primeiros pra não poluir)
def warn_invalid(invalid: list):
    if (len(invalid) == 0):
        return

    shown = ", ".join(f'"{token}"' for token in invalid[:5])
    extra = f" (e mais {len(invalid) - 5})" if (len(invalid) > 5) else ""
    print(f"Aviso: {len(invalid)} valor(es) inválido(s) ignorado(s): {shown}{extra}")


# -> -> -> -> -> -> -> -> -> ->
# <- Opção 1: dados digitados ->
# <- <- <- <- <- <- <- <- <- <-
def load_from_terminal():
    raw = input("\nDigite os valores separados por vírgula (ex: 18, 19.5, 22):\n> ")

    try:
        values, invalid = read_terminal(raw)
    except DataError as error:
        print(f"\nErro: {error}")
        return None

    print(f"\nDados recebidos com sucesso! (n = {len(values)} elementos)")
    warn_invalid(invalid)
    return values


# -> -> -> -> -> -> -> -> -> ->
# <- Opção 2: arquivo .csv ->
# <- <- <- <- <- <- <- <- <- <-
def load_from_csv():
    path = input("\nCaminho do arquivo .csv (ENTER para usar o data/example.csv):\n> ").strip().strip('"')
    if (path == ""):
        path = EXAMPLE_CSV

    try:
        values, invalid, header = read_csv(path)
    except FileNotFoundError:
        print(f"\nErro: arquivo não encontrado ({path}).")
        return None
    except IsADirectoryError:
        print(f"\nErro: isso é uma pasta, não um arquivo ({path}).")
        return None
    except PermissionError:
        print(f"\nErro: sem permissão para ler o arquivo ({path}).")
        return None
    except (DataError, csv.Error) as error:
        print(f"\nErro: {error}")
        return None

    print(f"\nArquivo carregado com sucesso! (n = {len(values)} elementos)")
    if (header is not None):
        print(f"Cabeçalho ignorado: {', '.join(header)}")
    warn_invalid(invalid)
    return values


# -> -> -> -> -> -> ->
# <- Menu principal ->
# <- <- <- <- <- <- <-
def menu():
    while (True):
        clear()
        print("=====================================================")
        print("   ANALISADOR ESTATÍSTICO - ENGENHARIA DE SOFTWARE")
        print("=====================================================")
        print("[1] Inserir dados via terminal (separados por vírgula)")
        print("[2] Carregar arquivo .csv")
        print("[0] Sair")

        option = input("\nEscolha a opção: ").strip()

        if (option == "1"):
            values = load_from_terminal()
        elif (option == "2"):
            values = load_from_csv()
        elif (option == "0"):
            clear()
            print("Até a próxima!")
            break
        else:
            input("\nOpção inválida. Aperte ENTER para tentar novamente.")
            continue

        if (values is not None):
            show_report(values)

        input("\nPressione ENTER para voltar ao menu.")
