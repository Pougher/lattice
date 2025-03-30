import pygame

class Menu:
    """
    Menu is a class that organizes items into a menu, where they can be chosen
        and interacted with
    """
    def __init__(self, screen, width, height, active = True):
        self.elements = {}
        self.screen = screen
        self.active = active

        self.width = width
        self.height = height

        self.transition_frames = 0
        self.transition_target = 0
        self.transition_colour = [0, 0, 0]
        self.transition_finished_func = None
        self.transitioning = False
        self.transition_surface = None

    def add_element(self, name, element):
        """
        Add element gets a new menu element and adds it to our list of pre-
        existing elements.
        """
        self.elements[name] = element

    def transition(self, num_frames, colour, finished_func):
        self.transition_frames = 0
        self.transition_target = num_frames
        self.transition_colour = colour
        self.transition_finished_func = finished_func
        self.transition_surface = pygame.Surface((self.width, self.height))
        self.transition_surface.set_alpha(0)
        self.transitioning = True
        self.transition_surface.fill(self.transition_colour)

    def get(self, name):
        return self.elements[name]

    def update(self, events, delta):
        if self.transitioning:
            self.transition_frames += 1
            self.transition_surface.set_alpha(
                (self.transition_frames / self.transition_target) * 255)
            if self.transition_frames == self.transition_target:
                self.transitioning = False
                self.transition_finished_func()
        else:
            for element in self.elements.values():
                if callable(getattr(element, "update", None)):
                    element.update(events, delta)

    def render(self):
        for element in self.elements.values():
            element.render(self.screen)
        if self.transitioning:
            self.screen.blit(self.transition_surface, [0, 0])
