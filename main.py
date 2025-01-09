from src.validator.syntax_validator import validate_syntax


def main():
    grammar = "a*aaba|(ba|v)((?:2))"
    is_valid, msg = validate_syntax(grammar)
    print(is_valid, msg)


if __name__ == "__main__":
    main()
