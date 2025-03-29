from emath import eqn_cache as ecache
import pygame

class MathRenderer:
    """
    MathRenderer Class: Rendering all of your mathematical expressions
    """
    def __init__(self, width, height):
        self.equation_cache = ecache.EquationCache()

        self.w = width
        self.h = height

        # positions holds information about the screenspace positions of all of
        # the loaded equations
        self.positions = []
        self.equations = []

    def add_scaled(self, latex, position):
        eqn, i = self.equation_cache.load_equation(latex)
        rect = eqn.get_rect()

        # if the width of the image is more than 4/5ths the size of the screen,
        # we need to scale it down
        if rect.w > self.w * 0.8:
            scale_factor = (4 * self.w) / (5 * rect.w)
            rect.w = int(scale_factor * rect.w)
            rect.h = int(scale_factor * rect.h)

        eqn = self.equation_cache.scale_equation(i, [rect.w, rect.h])

        self.positions.append(position)
        self.equations.append(eqn)

    def render(self, screen):
        for i, position in enumerate(self.positions):
            eqn = self.equation_cache.get(i)
            screen.blit(eqn, position)
