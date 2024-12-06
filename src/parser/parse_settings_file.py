def parse_settings(file_path):
    required_keys = {
        "probability_of_random_next_term",
        "probability_of_not_end_when_final_symbol_found",
        "max_length",
        "max_time",
        "count_from_lang",
        "count_not_from_lang"
    }
    settings = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if '=' not in line:
                    raise ValueError(f"Строка не соответствует формату 'ключ=значение': {line}")

                key, value = map(str.strip, line.split('=', 1))

                if not key or not value:
                    raise ValueError(f"Ключ или значение пустые в строке: {line}")

                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    raise ValueError(f"Значение не является числом в строке: {line}")

                settings[key] = value

        missing_keys = required_keys - settings.keys()
        if missing_keys:
            raise ValueError(f"Отсутствуют обязательные ключи: {', '.join(missing_keys)}")

        return settings

    except FileNotFoundError:
        raise ValueError(f"Файл '{file_path}' не найден.")
    except Exception as e:
        raise ValueError(f"Ошибка: {e}")
