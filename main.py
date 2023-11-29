# Numbered Production rules from CFG
grammar = {
    1: ["E", ["E", "+", "T"]],
    2: ["E", ["T"]],
    3: ["T", ["T", "*", "F"]],
    4: ["T", ["F"]],
    5: ["F", ["(", "E", ")"]],
    6: ["F", ["id"]],
}

# LR Parsing Table
parsing_table = {
    0: {"id": ("S", 5), "(": ("S", 4), "E": ("", 1), "T": ("", 2), "F": ("", 3)},
    1: {"$": ("A", "-> Accepted!"), "+": ("S", 6)},
    2: {"+": ("R", 2), "*": ("S", 7), ")": ("R", 2), "$": ("R", 2)},
    3: {"+": ("R", 4), "*": ("R", 4), ")": ("R", 4), "$": ("R", 4)},
    4: {"id": ("S", 5), "(": ("S", 4), "E": ("", 8), "T": ("", 2), "F": ("", 3)},
    5: {"+": ("R", 6), "*": ("R", 6), ")": ("R", 6), "$": ("R", 6)},
    6: {"id": ("S", 5), "(": ("S", 4), "T": ("", 9), "F": ("", 3)},
    7: {"id": ("S", 5), "(": ("S", 4), "F": ("", 10)},
    8: {"+": ("S", 6), ")": ("S", 11)},
    9: {"+": ("R", 1), "*": ("S", 7), ")": ("R", 1), "$": ("R", 1)},
    10: {"+": ("R", 3), "*": ("R", 3), ")": ("R", 3), "$": ("R", 3)},
    11: {"+": ("R", 5), "*": ("R", 5), ")": ("R", 5), "$": ("R", 5)},
}


# Function to parse the input string
def parse(input_string):
    stack = [0]  # Initialize stack with starting state
    pointer = 0  # Pointer to the current symbol in input_string
    if input_string[len(input_string) - 1] != "$":
        input_string += "$"

    while True:
        current_state = stack[-1]
        current_symbol = input_string[pointer]
        if current_symbol == "i":
            current_symbol += input_string[pointer + 1]
        action, value = parsing_table[current_state].get(current_symbol, ("", ""))

        print(
            f"Stack: {stack}, Input: {input_string[pointer:]}, Action: {action}{value}"
        )

        if action == "S":  # Shift
            stack.append(current_symbol)
            stack.append(value)
            if current_symbol == "id":
                pointer += 2
            else:
                pointer += 1
        elif action == "R":  # Reduce
            for _ in range(2 * len(grammar[value][1])):
                stack.pop()
            temp = stack[-1]
            stack.append(grammar[value][0])
            stack.append(parsing_table[temp][stack[-1]][1])
        elif action == "A":  # Accept
            return True
        else:
            return False  # Reject if no action is defined


# Test the parser with given strings
# test_strings = ["(id+id)*id$", "id*id$", "(id*)$"]
terminal_input = input("Please enter a string to parse: ")
# for string in test_strings:
print(f'\nParsing "{terminal_input}":')
result = parse(terminal_input)
print(f"Output: String is {'accepted' if result else 'not accepted'}.\n")
