from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from matplotlib import pyplot as plt
from typing import Union

def show(automata: Union[DFA, NFA]):
    automata.show_diagram().draw('images/automata.png', prog='dot')
    img = plt.imread('images/automata.png')
    plt.imshow(img)
    plt.show()