import pygame
import sympy
import random

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

class DifferentialQuestionManager:
    def __init__(self, screen, font):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.renderer = math_render.MathRenderer(self.width, self.height)
        self.equation_builder = make_eq.EquationBuilder()

        self.current_question = None
        self.current_answer = None
        self.difficulty_level = 3

        self.question_tween = None
        self.answer_tween = None

        self.solve_time = 0
        self.solving = True

        self.input_allowed_in = -1
        self.frame_counter = 0

        self.font = font

        # setup the font

        self.answer_input = Tween(TextInput(
            [ 0.05 * self.width, self.height * 0.6 ],
            self.width - 0.1 * self.width,
            self.font,
            20,
            (128, 128, 128),
            self.answer_entered
        ))
        self.answer_input.obj.set_opacity(1)

        self.init_text_objects()

    def init_text_objects(self):
        """
        This initializes all of the displayed text objects
        """
        self.text_displays = {
            "timer"     : Tween(
                Text('00:00:00.000', self.font, (0, 0), [230, 170, 30])),
            "pspace"    : Tween(
                Text('[Press Space when you are done]',
                     self.font, (0, 0), [64, 64, 64])),
            "anscheck"  : Tween(
                Text('Your answer was correct',
                     self.font, [0, 0], [32, 32, 32])),
            "nextq"     : Tween(
                Text("[Press Space for the next question]",
                     self.font, [20, 200], [64, 64, 64]))
        }

        self.text_displays['nextq'].obj.move(
            (self.width - self.text_displays['nextq'].obj.get_width()) / 2,
            self.height * 0.65 + 1 + self.font.get_height()
        )
        self.text_displays["nextq"].obj.active = False

    def generate_question(self):
        self.current_question = self.equation_builder.make_random_equation(
            self.difficulty_level
        )
        self.current_answer = sympy.diff(self.current_question)

        self.renderer.reset()
        self.question_tween = self.renderer.add_scaled(
            r"$" + sympy.latex(sympy.Derivative(self.current_question)) + "$",
            [0, 0.25 * self.height], center_x = True)
        self.question_tween.obj.set_opacity(1)
        self.question_tween.fade(240)

        # setup the text objects
        self.text_displays['timer'].obj.position = [
            (self.width - self.text_displays['timer'].obj.get_width()) / 2,
            0.6 * self.height
        ]
        self.text_displays['timer'].obj.colour = [32, 32, 32]
        self.text_displays['timer'].change_color([230, 170, 30], 240)

        self.text_displays['pspace'].obj.position = [
            (self.width - self.text_displays['pspace'].obj.get_width()) / 2,
            0.65 * self.height
        ]
        self.text_displays['nextq'].obj.colour = [32, 32, 32]
        self.text_displays['nextq'].obj.active = False

    def render(self):
        self.renderer.render(self.screen)

        # render the elapsed time
        self.text_displays['timer'].render(self.screen)

        # render the "press space when your done"
        self.text_displays['pspace'].render(self.screen)
        self.text_displays['anscheck'].render(self.screen)
        self.text_displays['nextq'].render(self.screen)

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

        # in addition to this, the text display should try and move 1 / 20th
        # of the screen resolution below the question
        timer_pos = self.text_displays['timer'].obj.position[1]
        target = (self.height * 0.1 - timer_pos) + \
            self.height * 0.05 + self.question_tween.obj.get_height()
        self.text_displays['timer'].wait_then(
            lambda x: x.move_sin(0, target, 480),
            240
        )
        self.text_displays['timer'].obj.colour = [140, 185, 50]

        # we also need to change the press space text to being invisible
        self.text_displays['pspace'].change_color([32, 32, 32], 480)

        # lets allow the user to input an answer
        self.answer_input.wait_then(
            lambda x: x.fade(240),
            480
        )
        self.input_allowed_in = 730
        self.frame_counter = 0

    def test_answer(self, expr):
        """
        one input isn't really enough, so we will test 10
        Reasoning: some functions given the same value of x can return the same
        value, despite not actually being equal.
        Also we never substitute zero because that causes issues sometimes
        """
        c = 0
        for i in range(10):
            v = random.randint(1, 100)
            try:
                if expr.subs({'x' : v}) == self.current_answer.subs({'x' : v}):
                    c += 1
            except:
                return (0, -1)

        return (c == 10, 0)

    def answer_entered(self, answer):
        """
        So the user has entered their answer. Lets turn this into a sympy
        expression and evaluate it, and compare it against the derivative
        """
        expr = None
        correct = None
        try:
            expr = sympy.sympify(answer)
            correct = self.test_answer(expr)

            if correct[1] != 0:
                print("Bad input")
                return
        except:
            print("Bad input")
            return

        if correct[0]:
            self.text_displays['anscheck'].obj.text = 'Your answer was correct'
            self.text_displays['anscheck'].wait_then(
                lambda x: x.change_color([140, 185, 50], 240),
                240)
        else:
            self.text_displays['anscheck'].obj.text = \
                'Your answer was not correct'
            self.text_displays['anscheck'].wait_then(
                lambda x: x.change_color([230, 50, 80], 240),
                240)


        self.text_displays['anscheck'].obj.position[0] = \
            (self.width - self.text_displays['anscheck'].obj.get_width()) / 2
        self.text_displays['anscheck'].obj.position[1] = self.height * 0.7
        self.text_displays['timer'].change_color([32, 32, 32], 240)

        self.answer_input.obj.active = False
        self.answer_input.fade(-240)

        answer_height = max(
            self.question_tween.obj.get_height(),
            0.4 * self.height)
        self.answer_tween = self.renderer.add_scaled(
            r"$" + sympy.latex(self.current_answer) + "$",
            [0, answer_height], center_x = True)
        self.answer_tween.obj.set_opacity(1.0)
        self.answer_tween.fade(480)

        self.text_displays['nextq'].obj.active = True
        self.text_displays['nextq'].wait_then(
            lambda x: x.change_color([64, 64, 64], 240),
            480
        )

    def handle_next_question(self):
        """
        Handles rerendering and resetting the question manager's state to
        prepare it for the next question
        """
        self.renderer.reset()
        self.answer_tween = None

        self.solving = True
        self.solve_time = 0

        self.init_text_objects()
        self.generate_question()

        self.answer_input.obj.reset()

    def update(self, events, delta):
        self.answer_input.update()
        self.answer_input.obj.update(events, delta)

        for text in self.text_displays.values():
            text.update()
        self.renderer.update(events)

        if self.solving and not self.text_displays['timer'].in_transition():
            self.solve_time += delta
            self.text_displays['timer'].obj.text = \
                convert_millis(self.solve_time)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.text_displays['nextq'].obj.active and not\
                    self.text_displays['nextq'].in_transition():
                    print('handling')
                    self.handle_next_question()
                    print(self.text_displays['nextq'].obj.active)
                elif self.solving and event.key == pygame.K_SPACE:
                    if not self.text_displays['timer'].in_transition():
                        self.on_finish_solving()
                else:
                    if self.answer_input.obj.active:
                        self.answer_input.obj.recieve_key_down(
                            event.key, event.unicode)
            if event.type == pygame.KEYUP:
                if self.answer_input.obj.active:
                    self.answer_input.obj.recieve_key_up(
                        event.key, event.unicode)

        # NOTE: This is done because of my stupid badly made tweening system.
        # Basically if you make inputs before a tweening animation has
        # finished, then a fun thing happens where everything crashes. Thus I
        # had to implement this 730 frame delay, which makes sure everything is
        # all fine before accepting input
        self.frame_counter += 1
        if self.frame_counter == self.input_allowed_in:
            self.input_allowed_in = -1
            self.answer_input.obj.active = True
