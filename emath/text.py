import pygame

class Text:
    """
    Text refers to a text object. It can be rendered to the screen and thats
    about it
    """
    def __init__(self, text, font, position, colour = [255, 255, 255]):
        self.text = text
        self.font = font
        self.position = position
        self.colour = colour

    def get_width(self):
        surf = self.font.render(self.text, True, self.colour)
        return surf.get_rect().w

    def render(self, screen):
        surf = self.font.render(self.text, True, self.colour)
        screen.blit(surf, self.position)

    def get_colour(self):
        return self.colour

    def move(self, x, y):
        self.position[0] += x
        self.position[1] += y
