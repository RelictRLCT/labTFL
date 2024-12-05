from src.cfg import CFG

# rules = {
#     "S": [["A", "B", "C"], ["B", "C"]],
#     "A": [["a", "B", "a"]],
#     "B": [["b"]],
#     "C": [["c"]],
#     "D": [["A", "D"]],  # Бесполезное
#     "E": [["A"]],       # Цепное
# }

rules = {
    "S": [["A", "B", "C", "D", "a"], ["B", "C", "C"], ["D"]],
    "A": [["B"]],
    "B": [["C"]],
    "C": [["c"]],
    "D": [["D"]]
}

start_symbol = "S"

cfg = CFG(rules, start_symbol)
print("Исходная грамматика:")
cfg.display()

cfg.convert_to_cnf()
print("\nГрамматика в ХНФ:")
cfg.display()
