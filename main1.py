import re

def input_grammar():
    grammar = {}
    while True:
        non_terminals = input("Enter the Non-Terminals separated by spaces: ").split()
        if all(nt.isalnum() for nt in non_terminals): 
            break
        else:
            print("Invalid input. Non-Terminals should be alphanumeric and separated by spaces.")
    for nt in non_terminals:
        print(f"Enter rule number 1 for non-terminal '{nt}': ", end="")
        rules = []
        rules.append(input().strip())
        print(f"Enter rule number 2 for non-terminal '{nt}': ", end="")
        rules.append(input().strip())
        grammar[nt] = rules
    return grammar


def is_simple_grammar(grammar):
    for nt, rules in grammar.items():
        for rule in rules:
            if re.search(r"[A-Z].*[A-Z]", rule): 
                return False
    return True


def parse_sequence(grammar, start_symbol, sequence):
    def parse(symbol, seq):
        if not seq and not symbol:
            return True
        if not seq or not symbol:
            return False
        if symbol[0].islower() or symbol[0].isdigit(): 
            if seq[0] == symbol[0]:
                return parse(symbol[1:], seq[1:])
            else:
                return False
        else:
            if symbol[0] in grammar:
                for rule in grammar[symbol[0]]:
                    if parse(rule + symbol[1:], seq):
                        return True
        return False

    return parse(start_symbol, sequence)


def main():
    grammar = {}
    while True:
        print("\nGrammars\n")
        command = input("Type 'new' to input new grammar, or 'check' to check a sequence: ").strip().lower()
        if command == 'new':
            grammar = input_grammar()
            if not is_simple_grammar(grammar):
                print("\nThe Grammar isn't simple.\n")
                print("Try again")
                continue
            else:
                print("\nThe Grammar is simple.\n")
            start_symbol = input("Enter the start symbol: ")
        elif command == 'check':
            if not grammar:
                print("Please input the grammar first by typing 'new'.")
                continue
            sequence = input("Enter the sequence to check (or 'change' to change grammar, 'exit' to quit): ").strip()
            if sequence == 'exit':
                break
            if sequence == 'change':
                grammar = input_grammar()
                if not is_simple_grammar(grammar):
                    print("\nThe Grammar isn't simple.\n")
                    print("Try again")
                    continue
                else:
                    print("\nThe Grammar is simple.\n")
                start_symbol = input("Enter the start symbol: ")
                continue
            if parse_sequence(grammar, start_symbol, sequence):
                print(f"The sequence {sequence} is accepted.")
            else:
                print(f"The sequence {sequence} is rejected.")
        else:
            print("Invalid command. Please type 'new' or 'check'.")


main()

