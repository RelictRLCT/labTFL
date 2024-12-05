from collections import defaultdict

class CFG:
    def __init__(self, rules: dict, start_symbol: str):
        """
        :param rules: Словарь, где ключи - нетерминалы, а значения - список продукций
        :param start_symbol: Стартовый символ
        """
        self.rules = rules
        self.start_symbol = start_symbol

    def remove_chain_rules(self):
        """
        Удаление цепных правил
        """
        chain_sets = defaultdict(set)

        # Множество нетерминалов, достижимых по цепным правилам
        for nt in self.rules:
            chain_sets[nt].add(nt)

        changed = True
        # Проходы до тех пор, пока множества цепных нетерминалов не перестанут изменяться
        while changed:
            #print(chain_sets)
            changed = False
            for nt in self.rules:
                for prod in self.rules[nt]:
                    # Если продукция - цепное правило (один нетерминал)
                    if len(prod) == 1 and prod[0].isupper(): #TODO: потом надо будет заменить на нормальную проверку
                        symbol = prod[0]
                        before = len(chain_sets[nt])
                        # Добавление к множеству нетерминалов нетерминалов, достижимых из symbol
                        chain_sets[nt].update(chain_sets[symbol])

                        if len(chain_sets[nt]) > before:
                            changed = True

        # Новые правила без цепных правил
        new_rules = defaultdict(list)
        for nt in self.rules:
            for chain_nt in chain_sets[nt]:
                for prod in self.rules[chain_nt]:
                    # Исключение цепных правил (добавление в исходный нетерминал продукций,
                    # получаемых из достижимых по цепным правилам нетерминалов)
                    if len(prod) != 1 or not prod[0].isupper(): #TODO: потом надо будет заменить на нормальную проверку
                        if prod not in new_rules[nt]:
                            new_rules[nt].append(prod)
        self.rules = new_rules

    def remove_useless_rules(self):
        """
        Удаление бесполезных правил:
        1) Непорождающие нетерминалы
        2) Недостижимые из стартового нетерминалы
        """
        # Поиск порождающих нетерминалов
        generating = set()
        changed = True
        while changed:
            changed = False
            for nt in self.rules:
                if nt in generating:
                    continue  # Уже среди порождающих
                for prod in self.rules[nt]:
                    # Если все символы в продукции - терминалы или порождающие нетерминалы
                    if all(symbol.islower() or symbol in generating for symbol in prod): #TODO: потом надо будет заменить на нормальную проверку
                        generating.add(nt)
                        changed = True
                        break  # Сразу можно к следующему

        # Поиск достижимых нетерминалов (как в поиске цепных правил)
        reachable = set([self.start_symbol])
        changed = True
        while changed:
            changed = False
            for nt in list(reachable):
                for prod in self.rules[nt]:
                    for symbol in prod:
                        # Если символ - нетерминал и еще не отмечен как достижимый
                        if symbol.isupper() and symbol not in reachable: #TODO: потом надо будет заменить на нормальную проверку
                            reachable.add(symbol)
                            changed = True

        # Только нужные нетерминалы останутся
        useful = generating & reachable
        new_rules = defaultdict(list)
        for nt in useful:
            for prod in self.rules[nt]:
                # Проверка, что все символы продукции - полезные нетерминалы или терминалы
                if all(symbol in useful or symbol.islower() for symbol in prod): #TODO: потом надо будет заменить на нормальную проверку
                    new_rules[nt].append(prod)
        self.rules = new_rules

    def reduce_long_rules(self):
        """
        Избавление от длинных правил
        """
        new_rules = defaultdict(list)
        new_symbol_index = 0

        for nt, productions in self.rules.items():
            for prod in productions:
                if len(prod) <= 2:
                    new_rules[nt].append(prod)  # Уже нормальное
                else:
                    symbols = prod
                    prev_symbol = nt
                    # Разбиение продукции на кучу правил
                    for i in range(len(symbols) - 1):
                        a = symbols[i]
                        if i < len(symbols) - 2:
                            # Новый нетерминал для промежуточных символов
                            new_nt = f"X{new_symbol_index}"
                            new_symbol_index += 1
                            new_rules[prev_symbol].append([a, new_nt])
                            prev_symbol = new_nt
                        else:
                            # Последние два символа
                            new_rules[prev_symbol].append([a, symbols[-1]])
        self.rules = new_rules

    def replace_terminals_in_rules(self):
        """
        Замена терминалов в продукциях длиной > 1 на нетерминалы
        """
        new_rules = defaultdict(list)
        terminal_map = {}  # Словарь для хранения соответствия терминалов новым нетерминалам
        new_symbol_index = 0

        for nt in self.rules:
            for prod in self.rules[nt]:
                if len(prod) == 1 and prod[0].islower(): #TODO: потом надо будет заменить на нормальную проверку
                    new_rules[nt].append(prod)  # Один терминал - нормально
                else:
                    new_prod = []
                    for symbol in prod:
                        if symbol.islower(): #TODO: потом надо будет заменить на нормальную проверку
                            # Если терминал уже заменен на нетерминал
                            if symbol not in terminal_map:
                                new_nt = f"G{new_symbol_index}"
                                new_symbol_index += 1
                                terminal_map[symbol] = new_nt
                                new_rules[terminal_map[symbol]].append([symbol])  # Добавление правила G -> a
                            new_prod.append(terminal_map[symbol])  # Замена терминала на нетерминал
                        else:
                            new_prod.append(symbol)
                    new_rules[nt].append(new_prod)

        for nt in new_rules:
            self.rules[nt] = new_rules[nt]

    def convert_to_cnf(self):
        """
        Преобразование грамматики в нормальную форму Хомского
        """
        self.remove_chain_rules()
        self.remove_useless_rules()
        self.reduce_long_rules()
        self.replace_terminals_in_rules()

    def display(self):
        """
        Вывод грамматики
        """
        for nt in self.rules:
            productions = self.rules[nt]
            prod_strings = [' '.join(prod) for prod in productions]
            print(f"{nt} -> {' | '.join(prod_strings)}")