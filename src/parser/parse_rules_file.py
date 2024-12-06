import re
from collections import defaultdict


def parse_grammar(file_content: str) -> (dict, list[str], list[str]):
    """
    Парсит грамматику из строки и возвращает словарь правил и списки терминалов и нетерминалов
    """
    rules = defaultdict(list)
    terms = set()
    nterms = []  # Чтоб сохранить стартовый нетерминал

    # Регулярные выражения для терминалов и нетерминалов
    nt_pattern = r'[A-Z][0-9]?|\[[A-Za-z]+[0-9]*\]'
    t_pattern = r'[a-z]'
    # Объединенный шаблон для символов
    symbol_pattern = re.compile(r'(' + nt_pattern + '|' + t_pattern + ')')

    # Регулярное выражение для всей строки правила
    rule_pattern = re.compile(r'^\s*(' + nt_pattern + r')\s*->\s*(.+)$')

    # Разбиение содержимого на строки
    lines = file_content.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Пустые строки

        match = rule_pattern.match(line)
        if not match:
            print(f"Ошибка разбора строки: {line}")
            return None, None, None

        left = match.group(1)
        right = match.group(2)

        if left not in nterms:
            nterms.append(left)  # Левая часть в список нетерминалов

        idx = 0
        length = len(right)
        production = []

        while idx < length:
            # Пропуск пробелов
            if right[idx].isspace():
                idx += 1
                continue

            symbol_match = symbol_pattern.match(right, idx)
            if symbol_match:
                symbol = symbol_match.group(1)
                if re.fullmatch(nt_pattern, symbol):
                    # Добавление нетерминала в список, если его ещё нет
                    if symbol not in nterms:
                        nterms.append(symbol)
                elif re.fullmatch(t_pattern, symbol):
                    terms.add(symbol)
                else:
                    print(f"Ошибка: некорректный символ '{symbol}' в строке {line}")
                    return None, None, None
                production.append(symbol)
                idx = symbol_match.end()
            else:
                print(f"Ошибка: неожиданный символ '{right[idx]}' в правой части правила на позиции {idx} в строке {line}")
                return None, None, None
        else:
            rules[left].append(production)

    terms = list(terms)

    return rules, terms, nterms
