from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from matplotlib import pyplot as plt
from typing import Union

from pathlib import Path

def show(automata: Union[DFA, NFA]):
    Path("images").mkdir(parents=True, exist_ok=True)
    automata.show_diagram().draw('images/labyrinth.png', prog='dot')
    img = plt.imread('images/labyrinth.png')
    plt.imshow(img)
    plt.show()
