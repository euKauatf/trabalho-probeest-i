# src/services/ungrouped.py

'''
PARTE 1 - Dados Não Agrupados
Regra do professor: aqui é OBRIGATÓRIO (e só pode) usar o pacote nativo statistics.
'''

import statistics # Importando o statistics, o único permitido nessa parte


# -> -> -> -> -> -> -> -> ->  -> -> -> -> -> ->
# <- Função que calcula média, mediana e moda ->
# <- <- <- <- <- <- <- <- <-  <- <- <- <- <- <-
def ungrouped_measures(values: list):
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "mode": statistics.mode(values) # Se tiver empate, o statistics devolve o primeiro que aparece nos dados
    }
