from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from generator import generate_labyrinth
from show import show

if __name__ == '__main__':

    labyrinth : DFA = generate_labyrinth()
    show(labyrinth)