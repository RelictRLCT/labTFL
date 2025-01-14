def validate_syntax(s: str) -> (bool, str):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyz123456789()|*?:\\")
    count_br = 0
    length = len(s)
    prev_char = None

    for i in range(0, length):
        char = s[i]
        # print(i, char, prev_char)

        if char not in allowed_chars:
            return False, f"Недопустимый символ '{char}', позиция {i}"

        if char.isdigit():
            if prev_char != '\\' and prev_char != '?':
                return False, f"Недопустимая цифра '{char}', позиция {i}"
            prev_char = char

        elif char == "\\":
            if i + 1 >= length:
                return False, f"Символ '\\' не может стоять в конце строки"
            next_char = s[i + 1]
            if not next_char.isdigit():
                return False, f"После '\\' должен идти номер группы, найден '{next_char}' в позиции {i + 1}."
            prev_char = char

        elif char == "(":
            count_br += 1
            if i + 1 < length and s[i + 1] in ('*', ')'):
                return False, f"Нельзя ставить '{s[i + 1]}' сразу после '(' в позиции {i + 1}."
            prev_char = char

        elif char == ")":
            if count_br == 0:
                return False, f'Закрывающая скобка без открывающей на позиции {i}'
            count_br -= 1
            prev_char = char

        elif char == "*":
            if prev_char in ("(", "|", None):
                return False, f"Недопустима '*' на позиции {i}"
            prev_char = char

        elif char == "|":
            if i == length - 1 or prev_char in ("(", "|", None):
                return False, f"'|' недопустима на позиции {i}"
            if s[i+1] in (")", "|"):
                return False, f"Альтернатива не должна быть пустой на позиции {i}"
            prev_char = char

        elif char == "?":
            if prev_char != "(":
                return False, f"'?' недопустим на позиции {i}"
            prev_char = char
        elif char == ":":
            if prev_char != "?":
                return False, f"':' недопустим на позиции {i}"
            prev_char = char
        else:
            prev_char = char

    if count_br == 0:
        return True, 'ОК!'
    else:
        return False, "Нарушен баланс скобок"
