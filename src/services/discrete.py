# src/services/discrete.py

'''
PARTE 2 - Dados Agrupados SEM Intervalo de Classe
Aqui os dados brutos viram uma tabela (xi | fi | Fi) e TODAS as medidas são tiradas da tabela,
nunca da lista original.
'''

from src.models.frequency import FrequencyRow # Importando a linha da tabela


# -> -> -> -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Função que monta a tabela de frequências ->
# <- <- <- <- <- <- <- <- <- <-  <- <- <- <- <- <-
def build_discrete_table(values: list):
    # Contando quantas vezes cada valor aparece (dicionário valor -> fi)
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1

    # Montando as linhas em ordem crescente e já acumulando o Fi
    table = []
    accumulated = 0
    for value in sorted(counts):
        accumulated += counts[value]
        table.append(FrequencyRow(value, counts[value], accumulated))

    return table


# -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Média ponderada: Σ(xi · fi) / n ->
# <- <- <- <- <- <- <-  <- <- <- <- <- <-
def discrete_mean(table: list):
    n = table[-1].Fi # O último Fi é o total de elementos

    total = 0
    for row in table:
        total += row.value * row.fi

    return total / n


# -> -> -> -> -> -> -> -> -> -> -> ->  -> -> -> -> ->
# <- Função auxiliar: qual xi ocupa a posição "p"? ->
# <- <- <- <- <- <- <- <- <- <- <- <-  <- <- <- <- <-
def value_at_position(table: list, position: int):
    # O primeiro Fi que alcança a posição é a linha onde o elemento está
    for row in table:
        if (row.Fi >= position):
            return row.value


# -> -> -> -> -> -> -> -> -> ->  -> -> -> -> ->
# <- Mediana pela frequência acumulada (Fi) ->
# <- <- <- <- <- <- <- <- <- <-  <- <- <- <- <-
def discrete_median(table: list):
    n = table[-1].Fi

    if (n % 2 == 1): # n ímpar -> elemento central na posição (n + 1) / 2
        return value_at_position(table, (n + 1) // 2)

    # n par -> média dos elementos nas posições n/2 e n/2 + 1
    return (value_at_position(table, n // 2) + value_at_position(table, n // 2 + 1)) / 2


# -> -> -> -> -> -> -> -> ->  -> -> ->
# <- Moda: o(s) xi de maior fi ->
# <- <- <- <- <- <- <- <- <-  <- <- <-
def discrete_mode(table: list):
    highest = 0
    for row in table:
        if (row.fi > highest):
            highest = row.fi

    modes = [row.value for row in table if row.fi == highest]

    # Se todo mundo tem a mesma frequência (e tem mais de um valor), não existe moda
    if (len(modes) == len(table) and len(table) > 1):
        return []

    return modes
