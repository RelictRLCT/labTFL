from automata.fa.dfa import DFA
from lab2.generator import generate_labyrinth
from lab2.show import show

if __name__ == '__main__':

    labyrinth : DFA = generate_labyrinth()
    show(labyrinth)