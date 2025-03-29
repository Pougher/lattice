import pygame
import sympy

import emath.math_render as math_render
import emath.make_eq as make_eq

def convert_millis(millis):
    """
    Convert milliseconds into hours, minutes, seconds and a fractional part,
    and then format it as a time string
    """
    seconds = int(millis / 1000) % 60
    minutes = int(millis / 60000) % 60
    hours   = int(millis / 3600000)
    millis = millis % 1000

    return "{:02d}:{:02d}:{:02d}.{:03d}".format(hours, minutes, seconds, millis)

class QuestionManager:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.renderer = math_render.MathRenderer(self.width, self.height)
        self.equation_builder = make_eq.EquationBuilder()

        self.current_question = None
        self.current_answer = None
        self.difficulty_level = 20
        self.solve_time = 0

        # setup the font
        self.font = pygame.font.Font('res/robotomono.ttf', 30)

    def generate_question(self):
        self.current_question = self.equation_builder.make_random_equation(
            self.difficulty_level
        )
        self.current_answer = sympy.diff(self.current_question)

        self.renderer.reset()
        self.renderer.add_scaled(
            r"$" + sympy.latex(sympy.Derivative(self.current_question)) + "$",
            [0, 0.25 * self.height], center_x = True)
        #self.renderer.add_scaled(
        #    r"$" + sympy.latex(self.current_answer) + "$", [0, 200])

    def render(self):
        self.renderer.render(self.screen)

        # render the elapsed time
        time = self.font.render(
            convert_millis(self.solve_time),
            True,
            (230, 170, 36)
        )
        self.screen.blit(time,
            ((self.width - time.get_rect().w) / 2, 0.5 * self.height))

        # render the "press space when your done"
        text = self.font.render(
            '[Press Space when you are done]',
            True,
            (64, 64, 64)
        )
        self.screen.blit(text,
            ((self.width - text.get_rect().w) / 2, 0.6 * self.height))

    def update(self, events, delta):
        self.renderer.update(events)
        self.solve_time += delta

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("OK")
