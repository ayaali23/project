import re

# إدخال الجرامر من المستخدم
def input_grammar():
    grammar = {}
    while True:
        # طلب الرموز غير النهائية
        non_terminals = input("Enter the Non-Terminals separated by spaces: ").split()
        if all(nt.isalnum() for nt in non_terminals):  # التحقق من أنها رموز صالحة
            break
        else:
            print("Invalid input. Non-Terminals should be alphanumeric and separated by spaces.")
    for nt in non_terminals:
        rules = []
        # طلب قاعدتين لكل رمز غير نهائي
        print(f"Enter rule number 1 for non-terminal '{nt}': ", end="")
        rules.append(input().strip())
        print(f"Enter rule number 2 for non-terminal '{nt}': ", end="")
        rules.append(input().strip())
        grammar[nt] = rules
    return grammar

# التحقق من بساطة الجرامر وفقًا للشروط الجديدة
def is_simple_grammar(grammar):
    for nt, rules in grammar.items():
        seen_start_symbols = set()  # لتتبع الرموز الأولية التي تبدأ بها القواعد
        for rule in rules:
            if rule == '':  # الشرط الثاني: لا يمكن أن تكون القاعدة إبسيلون
                return False
            if not rule[0].islower() and not rule[0].isdigit():  # الشرط الأول: يجب أن تبدأ بـ Terminal
                return False
            if rule[0] in seen_start_symbols:  # الشرط الثالث: لا يمكن تكرار الرموز الأولية
                return False
            seen_start_symbols.add(rule[0])
    return True

# التحقق من قبول سلسلة بناءً على قواعد الجرامر
def parse_sequence(grammar, start_symbol, sequence):
    def parse(symbol, seq):
        if not seq and not symbol:  # إذا انتهت السلسلة والرموز
            return True
        if not seq or not symbol:  # إذا انتهت السلسلة فقط أو الرموز فقط
            return False
        if symbol[0].islower() or symbol[0].isdigit():  # إذا كان الرمز Terminal
            if seq[0] == symbol[0]:
                return parse(symbol[1:], seq[1:])  # التحقق من المطابقة والاستمرار
            else:
                return False
        else:  # إذا كان الرمز Non-Terminal
            if symbol[0] in grammar:
                for rule in grammar[symbol[0]]:  # تطبيق القواعد المرتبطة به
                    if parse(rule + symbol[1:], seq):
                        return True
        return False

    return parse(start_symbol, sequence)

# واجهة المستخدم
def main():
    grammar = {}
    while True:
        print("\nGrammars\n")
        # أوامر المستخدم
        command = input("Type 'new' to input new grammar, or 'check' to check a sequence: ").strip().lower()
        if command == 'new':  # إدخال جرامر جديد
            grammar = input_grammar()
            if not is_simple_grammar(grammar):  # التحقق من البساطة
                print("\nThe Grammar isn't simple.\n")
                print("Try again")
                continue
            else:
                print("\nThe Grammar is simple.\n")
            start_symbol = input("Enter the start symbol: ")  # تحديد رمز البداية
        elif command == 'check':  # التحقق من سلسلة
            if not grammar:
                print("Please input the grammar first by typing 'new'.")
                continue
            sequence = input("Enter the sequence to check (or 'change' to change grammar, 'exit' to quit): ").strip()
            if sequence == 'exit':
                break
            if sequence == 'change':  # تغيير الجرامر
                grammar = input_grammar()
                if not is_simple_grammar(grammar):
                    print("\nThe Grammar isn't simple.\n")
                    print("Try again")
                    continue
                else:
                    print("\nThe Grammar is simple.\n")
                start_symbol = input("Enter the start symbol: ")
                continue
            if parse_sequence(grammar, start_symbol, sequence):  # التحقق من قبول السلسلة
                print(f"The sequence {sequence} is accepted.")
            else:
                print(f"The sequence {sequence} is rejected.")
        else:
            print("Invalid command. Please type 'new' or 'check'.")

main()