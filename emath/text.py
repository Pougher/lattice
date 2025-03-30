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
        self.active = True

    def get_width(self):
        return self.font.size(self.text)[0]

    def render(self, screen):
        if self.active:
            surf = self.font.render(self.text, True, self.colour)
            screen.blit(surf, self.position)

    def get_colour(self):
        return self.colour

    def move(self, x, y):
        self.position[0] += x
        self.position[1] += y
