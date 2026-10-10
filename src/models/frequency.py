# src/models/frequency.py

# Classe FrequencyRow -> Uma linha da tabela SEM intervalo de classe (Parte 2)
class FrequencyRow:
    def __init__(self, value: float, fi: int, Fi: int):
        self.value = value # xi -> o valor em si
        self.fi = fi # Frequência absoluta (quantas vezes o valor aparece)
        self.Fi = Fi # Frequência acumulada (soma das fi até aqui)


# Classe ClassInterval -> Uma linha da tabela COM intervalo de classe (Parte 3)
class ClassInterval:
    def __init__(self, lower: float, upper: float, fi: int, Fi: int, closed: bool = False):
        self.lower = lower # Limite inferior (Li)
        self.upper = upper # Limite superior (Ls)
        self.fi = fi
        self.Fi = Fi
        self.closed = closed # True só na última classe, pra ela incluir o valor máximo [Li - Ls]

    # Amplitude da classe (h)
    def width(self):
        return self.upper - self.lower

    # Ponto médio da classe (xi), que é o que representa a classe na média
    def midpoint(self):
        return (self.lower + self.upper) / 2
