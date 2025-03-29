import pygame

class SurfaceWrapper:
    """
    SurfaceWrapper: Wrap all of your surfaces in bubblewrap
    Contains information about the position of a surface. Exclusively used to
    interact with Tween
    """
    def __init__(self, surf, position):
        self.surface = surf
        self.position = position

    def get_height(self):
        return self.surface.get_rect().h

    def render(self, screen):
        screen.blit(self.surface, self.position)

    def move(self, x, y):
        self.position[0] += x
        self.position[1] += y
