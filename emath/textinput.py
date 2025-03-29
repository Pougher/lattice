import pygame

class TextInput:
    def __init__(self, position, width, height, font, font_size, color):
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size
        self.position = position
        self.colour = color

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.colour,
            [ self.position[0], self.position[1], self.width, self.height ],
            4,
            border_radius = 8
        )
