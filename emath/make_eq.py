import sympy
import random

difficulty_function_set = {
    1: [],
    2: [ sympy.sin ],
    3: [ sympy.sin, sympy.cos ],
    4: [ sympy.sin, sympy.cos, sympy.tan ]
}

class EquationBuilder:
    def __init__(self):
        self.x = sympy.Symbol('x')
        self.operators = []
        self.functions = []
        self.difficulty = 0

        self.difficulty_operator_set = {
            1: [ self.operator_add, self.operator_sub ],
            2: [
                self.operator_add,
                self.operator_sub,
                self.operator_div,
                self.operator_mul],
            3: [
                self.operator_add, self.operator_sub, self.operator_div,
                self.operator_mul
            ]
        }

    def operator_mul(self, depth):
        if depth == 0:
            return self.x ** 2
        return (self.random_operator(depth - 1)) * \
               (self.random_operator(depth - 2))

    def operator_div(self, depth):
        return (self.random_operator(depth - 1)) / \
               (self.random_operator(depth - 2))

    def operator_sub(self, depth):
        return (self.random_operator(depth - 1)) - \
               (self.random_operator(depth - 2))

    def operator_add(self, depth):
        return (self.random_operator(depth - 1)) - \
               (self.random_operator(depth - 2))

    def random_operator(self, depth):
        if depth <= 0:
            return self.x ** random.randint(0, min(self.difficulty, 3))

        return (random.choice(self.operators)(depth - 1))

    def make_random_equation(self, difficulty):
        self.functions = difficulty_function_set[
                min(max(difficulty, 1), len(difficulty_function_set.keys()))]
        self.operators = self.difficulty_operator_set[
                min(max(difficulty, 1), len(self.difficulty_operator_set.keys()))]
        self.difficulty = difficulty

        expr = self.random_operator(difficulty + 1)
        print(expr)
        return expr
