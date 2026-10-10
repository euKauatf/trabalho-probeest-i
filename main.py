# main.py

from src.utils.interface import menu # Importando o menu principal
from src.utils.terminal import clear # Importando a função de limpar o terminal


# -> -> -> -> -> -> -> -> -> -> -> -> ->
# <- Função que dá a partida no programa ->
# <- <- <- <- <- <- <- <- <- <- <- <- <-
def main():
    try:
        menu()
    except (KeyboardInterrupt, EOFError): # Ctrl+C ou Ctrl+Z não estouram erro na cara do usuário
        clear()
        print("Programa encerrado. Até a próxima!")


if __name__ == "__main__":
    main()
