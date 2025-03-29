import pygame
import sympy

import emath.math_render as math_render
import emath.make_eq as make_eq
from emath.tween import Tween
from emath.text import Text
from emath.textinput import TextInput

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
        self.difficulty_level = 18

        self.question_tween = None
        self.answer_tween = None

        self.solve_time = 0
        self.solving = True

        # setup the font
        self.font = pygame.font.Font('res/robotomono.ttf', 30)

        self.answer_input = Tween(TextInput(
            [ 20, 20 ],
            200,
            100,
            self.font,
            20,
            (64, 64, 64)
        ))

        self.text_displays = {
            "timer" : Tween(
                Text('00:00:00.000', self.font, (0, 0), [230, 170, 30])),
            "pspace": Tween(
                Text('[Press Space when you are done]',
                     self.font, (0, 0), [64, 64, 64]))
        }

    def generate_question(self):
        self.current_question = self.equation_builder.make_random_equation(
            self.difficulty_level
        )
        self.current_answer = sympy.diff(self.current_question)

        self.renderer.reset()
        self.question_tween = self.renderer.add_scaled(
            r"$" + sympy.latex(sympy.Derivative(self.current_question)) + "$",
            [0, 0.25 * self.height], center_x = True)

        # setup the text objects
        self.text_displays['timer'].obj.position = [
            (self.width - self.text_displays['timer'].obj.get_width()) / 2,
            0.6 * self.height
        ]
        self.text_displays['pspace'].obj.position = [
            (self.width - self.text_displays['pspace'].obj.get_width()) / 2,
            0.65 * self.height
        ]
        #self.renderer.add_scaled(
        #    r"$" + sympy.latex(self.current_answer) + "$", [0, 200])

    def render(self):
        self.renderer.render(self.screen)

        # render the elapsed time
        self.text_displays['timer'].render(self.screen)

        # render the "press space when your done"
        self.text_displays['pspace'].render(self.screen)

        self.answer_input.render(self.screen)

    def on_finish_solving(self):
        """
        This handles all of the animations between the solving phase and the
        answering phase
        """
        self.solving = False
        # the question tween should move to the top 1/10th of the
        # screen, so calculate the difference from its current
        # position to the top tenth
        change = self.height * 0.1 - \
            self.question_tween.obj.position[1]
        self.question_tween.wait_then(
            lambda x: x.move_sin(0, change, 480),
            240
        )
        print(change)

        # in addition to this, the text display should try and move 1 / 20th
        # of the screen resolution below the question
        timer_pos = self.text_displays['timer'].obj.position[1]
        target = (self.height * 0.1 - timer_pos) + \
            self.height * 0.05 + self.question_tween.obj.get_height()
        self.text_displays['timer'].wait_then(
            lambda x: x.move_sin(0, target, 480),
            240
        )
        self.text_displays['timer'].obj.colour = (140, 185, 50)

        # we also need to change the press space text to being invisible
        self.text_displays['pspace'].change_color([32, 32, 32], 480)

    def update(self, events, delta):
        self.renderer.update(events)
        for text in self.text_displays.values():
            text.update()

        if self.solving:
            self.solve_time += delta
            self.text_displays['timer'].obj.text = \
                convert_millis(self.solve_time)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.on_finish_solving()
