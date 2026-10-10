# src/utils/report.py

from src.services.ungrouped import ungrouped_measures
from src.services.discrete import build_discrete_table, discrete_mean, discrete_median, discrete_mode
from src.services.grouped import (
    build_class_table, grouped_mean, grouped_median, czuber_mode, king_mode,
    quartile, decile, percentile
)

LINE = "-----------------------------------------------------"


# Formata com 2 casas, igual ao exemplo do professor
def fmt(number: float):
    return f"{number:.2f}"


# Formata o xi da Parte 2 sem casas desnecessárias (18 em vez de 18.00)
def fmt_value(number: float):
    return f"{number:g}"


def title(text: str):
    print(f"\n{LINE}\n{text}\n{LINE}")


# -> -> -> -> -> -> -> -> ->
# <- PARTE 1 na tela ->
# <- <- <- <- <- <- <- <- <-
def show_ungrouped(values: list):
    measures = ungrouped_measures(values)

    title("PARTE 1: DADOS NÃO AGRUPADOS (Módulo Statistics)")
    print(f"Média: {fmt(measures['mean'])}")
    print(f"Mediana: {fmt(measures['median'])}")
    print(f"Moda: {fmt(measures['mode'])}")


# -> -> -> -> -> -> -> -> ->
# <- PARTE 2 na tela ->
# <- <- <- <- <- <- <- <- <-
def show_discrete(values: list):
    table = build_discrete_table(values)

    title("PARTE 2: DISTRIBUIÇÃO DE FREQUÊNCIA (SEM INTERVALO)")
    print(f"{'Valor (xi)':^12}|{'Freq. Absoluta (fi)':^21}|{'Freq. Acumulada (Fi)':^22}")
    for row in table:
        print(f"{fmt_value(row.value):^12}|{row.fi:^21}|{row.Fi:^22}")

    modes = discrete_mode(table)
    if (len(modes) == 0):
        mode_text = "Amodal"
    else:
        mode_text = ", ".join(fmt(mode) for mode in modes)
        if (len(modes) > 1):
            mode_text += " (multimodal)"

    print(f"\nCalculados via tabela: Média = {fmt(discrete_mean(table))} | "
          f"Mediana = {fmt(discrete_median(table))} | Moda = {mode_text}")


# -> -> -> -> -> -> -> -> ->
# <- PARTE 3 na tela ->
# <- <- <- <- <- <- <- <- <-
def show_grouped(values: list):
    table, k, total_range, h = build_class_table(values)

    title("PARTE 3: DISTRIBUIÇÃO DE FREQUÊNCIA (COM INTERVALO)")
    print(f"n = {len(values)} | k (Sturges) = {k} | AT = {fmt(total_range)} | h = {fmt(h)}\n")

    # Montando o texto das classes primeiro pra alinhar a coluna pelo maior
    labels = []
    for row in table:
        closing = "]" if row.closed else ")"
        labels.append(f"[{fmt(row.lower)} - {fmt(row.upper)}{closing}")
    width = max(len(label) for label in labels + ["Classe"])

    print(f"{'Classe':<{width}} | {'fi':<4} | Fi")
    for label, row in zip(labels, table):
        print(f"{label:<{width}} | {row.fi:<4} | {row.Fi}")

    print("\nCalculados via Fórmulas de Interpolação:")
    print(f"-> Média: {fmt(grouped_mean(table))}    | Mediana: {fmt(grouped_median(table))}    | "
          f"Moda (Czuber): {fmt(czuber_mode(table))} | Moda (King): {fmt(king_mode(table))}")
    print(f"-> Quartis: Q1 = {fmt(quartile(table, 1))} | Q3 = {fmt(quartile(table, 3))}")
    print(f"-> Decis: D2 = {fmt(decile(table, 2))} | D7 = {fmt(decile(table, 7))}")
    print(f"-> Percentis: P15 = {fmt(percentile(table, 15))} | P22 = {fmt(percentile(table, 22))} | "
          f"P63 = {fmt(percentile(table, 63))} | P70 = {fmt(percentile(table, 70))}")


# Mostra as três partes de uma vez
def show_report(values: list):
    show_ungrouped(values)
    show_discrete(values)
    show_grouped(values)
