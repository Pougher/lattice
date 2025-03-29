import sympy
import random

difficulty_function_set = {
    1 : [], 2 : [], 3 : [], 4 : [],
    5 : [ sympy.sin ],
    6 : [ sympy.sin ],
    7 : [ sympy.sin, sympy.cos ],
    8 : [ sympy.sin, sympy.cos, sympy.tan ],
    9 : [ sympy.sin, sympy.cos, sympy.tan, sympy.ln, sympy.sec ],
    10: [ sympy.sin, sympy.cos, sympy.tan, sympy.ln, sympy.sec, sympy.csc,
          sympy.cot ]
}

class EquationBuilder:
    def __init__(self):
        self.x = sympy.Symbol('x')
        self.operators = []
        self.functions = []
        self.weights = []
        self.difficulty = 0

        self.difficulty_operator_set = {
            1 : [ self.operator_add, self.operator_sub ],
            2 : [ self.operator_add, self.operator_sub ],
            3 : [ self.operator_add, self.operator_sub ],
            4 : [ self.operator_add, self.operator_sub, self.operator_exp ],
            5 : [ self.operator_add, self.operator_sub, self.operator_exp,
                  self.operator_fn ],
            6 : [ self.operator_add, self.operator_sub, self.operator_exp,
                  self.operator_fn, self.operator_mul ],
            7 : [ self.operator_add, self.operator_sub, self.operator_exp,
                  self.operator_fn, self.operator_div, self.operator_mul ],
        }
        self.probabilities = {
            1 : [ 0.5, 0.5 ],
            2 : [ 0.5, 0.5 ],
            3 : [ 0.5, 0.5 ],
            4 : [ 0.4, 0.4, 0.2 ],
            5 : [ 0.2, 0.2, 0.2, 0.4 ],
            6 : [ 0.2, 0.2, 0.2, 0.3, 0.1 ],
            7 : [ 0.1, 0.1, 0.2, 0.35, 0.2, 0.15 ]
        }

    def operator_add(self, depth):
        if depth <= 1:
            return 1 + random.randint(min(2, self.difficulty), 5) * self.x

        return (self.random_operator(depth - 1)) + \
               (self.random_operator(depth - 2))

    def operator_sub(self, depth):
        if depth <= 1:
            return 1 - random.randint(min(2, self.difficulty), 5) * self.x

        return (self.random_operator(depth - 1)) - \
               (self.random_operator(depth - 2))

    def operator_exp(self, depth):
        return self.random_operator(depth - 1) ** \
                random.randint(2, min(self.difficulty, 5))

    def operator_mul(self, depth):
        if depth <= 1:
            return random.randint(min(2, self.difficulty), 5) * self.x

        return (self.random_operator(depth - 1)) * \
               (self.random_operator(depth - 2))

    def operator_div(self, depth):
        if depth <= 1:
            return random.randint(min(2, self.difficulty), 5) * self.x

        return (self.random_operator(depth - 1)) / \
               (self.random_operator(depth - 2))

    def operator_fn(self, depth):
        if depth <= 1:
            return self.x

        return random.choice(self.functions)(self.random_operator(depth - 1))

    def random_operator(self, depth):
        if depth <= 1:
            return self.x ** random.randint(1, min(3, self.difficulty))

        pick = random.choices(
            population = self.operators,
            weights = self.weights,
            k = 1)[0]
        return pick(depth - 1)

    def check_inf(self, expr):
        try:
            return expr.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan)
        except:
            return False

    def make_random_equation(self, difficulty):
        self.functions = difficulty_function_set[
                min(max(difficulty, 1), len(difficulty_function_set.keys()))]
        self.operators = self.difficulty_operator_set[
                min(max(difficulty, 1), len(self.difficulty_operator_set.keys()))]
        self.weights = self.probabilities[
                min(max(difficulty, 1), len(self.probabilities.keys()))]
        self.difficulty = difficulty

        # sometimes the expression can evaluate to zero, so in order to prevent
        # this we will loop until expr no longer evaluates to 0
        expr = 0
        while expr == 0 and not self.check_inf(expr) and not self.check_inf(sympy.diff(expr)):
            if difficulty >= 8:
                self.difficulty = difficulty - 2
            expr = self.random_operator(self.difficulty)

        print(expr)
        return expr
