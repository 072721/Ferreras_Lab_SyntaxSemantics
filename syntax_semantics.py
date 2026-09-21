# CS413 Laboratory Activity No. 2
# From Syntax to Semantics: Building a Grammar Checker and Evaluator

class Parser:
    def __init__(self, text):
        self.text = text.replace(" ", "")
        self.position = 0

    # Return the current character
    def current(self):
        if self.position < len(self.text):
            return self.text[self.position]
        return None

    # Move to the next character
    def advance(self):
        self.position += 1

    # ----------------------------------------
    # EXPR
    # <expr> -> <term> { (+ | -) <term> }
    # ----------------------------------------
    def expr(self):
        value = self.term()

        while self.current() in ('+', '-'):
            operator = self.current()
            self.advance()

            right = self.term()

            if operator == '+':
                value = value + right
            else:
                value = value - right

        return value

    # ----------------------------------------
    # TERM
    # <term> -> <factor> { (* | /) <factor> }
    # ----------------------------------------
    def term(self):
        value = self.factor()

        while self.current() in ('*', '/'):
            operator = self.current()
            self.advance()

            right = self.factor()

            if operator == '*':
                value = value * right
            else:
                if right == 0:
                    raise ValueError("Division by zero")
                value = value / right

        return value

    # ----------------------------------------
    # FACTOR
    # <factor> -> ( <expr> ) | <digit>
    # ----------------------------------------
    def factor(self):
        current = self.current()

        # Case 1: Digit
        if current is not None and current.isdigit():
            value = int(current)
            self.advance()
            return value

        # Case 2: Opening parenthesis
        elif current == '(':
            self.advance()

            # RECURSION:
            # factor calls expr when it finds '('
            value = self.expr()

            # The expression must have a closing parenthesis
            if self.current() != ')':
                raise SyntaxError(
                    f"Missing ')' at position {self.position}"
                )

            self.advance()
            return value

        # Invalid input
        else:
            if current is None:
                raise SyntaxError(
                    f"Unexpected end of input at position {self.position}"
                )
            else:
                raise SyntaxError(
                    f"Unexpected '{current}' at position {self.position}"
                )

    # ----------------------------------------
    # START PARSING
    # ----------------------------------------
    def parse(self):
        if self.text == "":
            raise SyntaxError("Input is empty")

        result = self.expr()

        # There should be no leftover characters
        if self.current() is not None:
            raise SyntaxError(
                f"Unexpected '{self.current()}' at position {self.position}"
            )

        return result


# ----------------------------------------
# AMBIGUITY DEMONSTRATION
# ----------------------------------------

print("==============================================")
print(" AMBIGUITY DEMONSTRATION")
print("==============================================")

print("Expression: 2+3*4")
print("Left-to-right evaluation: 20")
print("Normal precedence evaluation: 14")

print("\nThe corrected grammar gives * and / higher")
print("precedence than + and -.")
print("Therefore, 2+3*4 is evaluated as 2+(3*4) = 14.")


# ----------------------------------------
# REQUIRED TEST CASES
# ----------------------------------------

test_cases = [
    "3+4*2",
    "(3+4)*2",
    "8/2-1",
    "3++4",
    "(3+4",
    "2+3*4"
]

print("\n==============================================")
print(" REQUIRED TEST CASES")
print("==============================================")


for expression in test_cases:

    print(f"\nInput: {expression}")

    try:
        parser = Parser(expression)

        # Syntax checking + evaluation
        result = parser.parse()

        print("Syntax: Valid")
        print(f"Value: {result}")

    except (SyntaxError, ValueError) as error:

        print("Syntax: Invalid")
        print(f"Error: {error}")