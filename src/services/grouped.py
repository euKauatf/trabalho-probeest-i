# src/services/grouped.py

'''
PARTE 3 - Dados Agrupados COM Intervalo de Classe
Regra do professor: PROIBIDO usar statistics, pandas, numpy, scipy...
Tudo aqui é fórmula clássica feita no braço. O único import é o math, que não é biblioteca
estatística: ele só entra pra calcular o log10 da Fórmula de Sturges.
'''

import math # Importando math só pro log10

from src.models.frequency import ClassInterval # Importando a linha da tabela com intervalo

DECIMALS = 10 # Casas usadas pra arredondar os limites e fugir do erro de ponto flutuante (0.1 + 0.2...)


# -> -> -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Sturges: k = 1 + 3.322 · log10(n) ->
# <- <- <- <- <- <- <- <- <-  <- <- <- <- <- <-
def sturges(n: int):
    k = 1 + 3.322 * math.log10(n)
    return int(k + 0.5) # Arredondando pro inteiro mais próximo


# -> -> -> -> -> -> -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Função que monta a tabela de classes dinamicamente ->
# <- <- <- <- <- <- <- <- <- <- <- <- <-  <- <- <- <- <- <-
def build_class_table(values: list):
    n = len(values)
    smallest = min(values)
    largest = max(values)
    total_range = largest - smallest # Amplitude total (AT)

    if (total_range == 0): # Todos os valores iguais -> uma classe só, de amplitude 1
        k = 1
        h = 1
    else:
        k = sturges(n)
        h = total_range / k # Amplitude do intervalo (h = AT / k)

    table = []
    accumulated = 0
    for i in range(k):
        last = (i == k - 1)
        lower = round(smallest + i * h, DECIMALS)
        upper = round(smallest + (i + 1) * h, DECIMALS)

        # Classes no formato [Li - Ls), e a última fechada [Li - Ls] pra incluir o maior valor
        fi = 0
        for value in values:
            if (lower <= value < upper or (last and value == upper)):
                fi += 1

        accumulated += fi
        table.append(ClassInterval(lower, upper, fi, accumulated, closed=last))

    return table, k, total_range, h


# -> -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Média: x̄ = Σ(fi · xi) / n, xi = ponto médio ->
# <- <- <- <- <- <- <- <-  <- <- <- <- <- <-
def grouped_mean(table: list):
    n = table[-1].Fi

    total = 0
    for row in table:
        total += row.fi * row.midpoint()

    return total / n


# -> -> -> -> -> -> -> -> -> -> -> -> ->  -> -> -> -> ->
# <- Separatriz genérica (serve pra mediana, Q, D e P) ->
# <- <- <- <- <- <- <- <- <- <- <- <- <-  <- <- <- <- <-
'''
Fórmula da interpolação:  S = Li + ((posição - Fant) / fi) · h
- posição = (k · n) / partes  ->  partes = 2 (mediana), 4 (quartil), 10 (decil), 100 (percentil)
- Li = limite inferior da classe onde a posição cai
- Fant = frequência acumulada da classe ANTERIOR
- fi = frequência da classe da separatriz
- h = amplitude da classe
'''
def separatrix(table: list, k: int, parts: int):
    n = table[-1].Fi
    position = (k * n) / parts # Multiplicando antes de dividir pra não perder precisão (0.7 * 10 = 7.000000000000001)

    previous_F = 0
    for row in table:
        if (row.Fi >= position): # Achamos a classe da separatriz
            return row.lower + ((position - previous_F) / row.fi) * row.width()
        previous_F = row.Fi


def grouped_median(table: list):
    return separatrix(table, 1, 2) # Mediana = Q2 = D5 = P50


def quartile(table: list, k: int):
    return separatrix(table, k, 4)


def decile(table: list, k: int):
    return separatrix(table, k, 10)


def percentile(table: list, k: int):
    return separatrix(table, k, 100)


# -> -> -> -> -> -> -> -> ->  -> -> -> -> ->
# <- Função auxiliar: classe modal e vizinhas ->
# <- <- <- <- <- <- <- <- <-  <- <- <- <- <-
def modal_class(table: list):
    # A classe modal é a de maior fi (se empatar, fica a primeira)
    index = 0
    for i in range(len(table)):
        if (table[i].fi > table[index].fi):
            index = i

    f_previous = table[index - 1].fi if (index > 0) else 0 # Classe anterior (0 se não existir)
    f_next = table[index + 1].fi if (index < len(table) - 1) else 0 # Classe posterior (0 se não existir)

    return table[index], f_previous, f_next


# -> -> -> -> -> -> -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Moda de Czuber: Mo = Li + (Δ1 / (Δ1 + Δ2)) · h ->
# <- <- <- <- <- <- <- <- <- <- <- <- <-  <- <- <- <- <- <-
def czuber_mode(table: list):
    row, f_previous, f_next = modal_class(table)
    d1 = row.fi - f_previous # Δ1 = fi da modal - fi da anterior
    d2 = row.fi - f_next # Δ2 = fi da modal - fi da posterior

    if (d1 + d2 == 0): # Sem diferença pras vizinhas -> usa o ponto médio (moda bruta)
        return row.midpoint()

    return row.lower + (d1 / (d1 + d2)) * row.width()


# -> -> -> -> -> -> -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Moda de King: Mo = Li + (fpost / (fant + fpost)) · h ->
# <- <- <- <- <- <- <- <- <- <- <- <- <-  <- <- <- <- <- <-
def king_mode(table: list):
    row, f_previous, f_next = modal_class(table)

    if (f_previous + f_next == 0):
        return row.midpoint()

    return row.lower + (f_next / (f_previous + f_next)) * row.width()
