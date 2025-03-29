from emath import eqn_cache as ecache
import emath.slider as slider
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
        self.sliders = []

    def add_scaled(self, latex, position, center_x = False):
        """
        Adds an equation either to the equation cache, and rendering cache, or
        to a slider list in the case that the equation is too big to be
        rendered and still be readable.
        """
        eqn, i = self.equation_cache.load_equation(latex)
        rect = eqn.get_rect()

        # if the width of the image is more than 4/5ths the size of the screen,
        # we need to scale it down
        if rect.w <= 2 * self.w:
            if rect.w > self.w * 0.8:
                scale_factor = (4 * self.w) / (5 * rect.w)
                rect.w = int(scale_factor * rect.w)
                rect.h = int(scale_factor * rect.h)
            eqn = self.equation_cache.scale_equation(i, [rect.w, rect.h])

            if center_x:
                position[0] = (self.w - rect.w) / 2

            self.positions.append(position)
            self.equations.append(eqn)
        elif rect.w > 2 * self.w:
            # too large horizontally, but still scale vertically by a factor of
            # 1/2
            eqn = self.equation_cache.scale_equation(
                i, [rect.w / 2, rect.h / 2])
            if center_x:
                position[0] = 50
            self.sliders.append(slider.Slider(eqn, position, self.w - 100))

    def reset(self):
        """
        Reset does what it says it does: resets the positions, equations and
        sliders
        """
        self.positions = []
        self.equations = []
        self.sliders = []
        self.equation_cache.unload_all()

    def render(self, screen):
        """
        Renders all of the currently loaded equations and sliders to the screen
        """
        for i, position in enumerate(self.positions):
            eqn = self.equation_cache.get(i)
            screen.blit(eqn, position)

        for slider in self.sliders:
            slider.render(screen)

    def update(self, events):
        """
        Update checks all of the events and tests for a MOUSEBUTTONDOWN etc.
        and passes it on to the sliders.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for slider in self.sliders: slider.clickdown(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for slider in self.sliders: slider.clickup()
            elif event.type == pygame.MOUSEMOTION:
                for slider in self.sliders: slider.mousemotion(event.pos)
