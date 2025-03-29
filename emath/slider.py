import pygame

class Slider:
    """
    Slider is a class that can be used to simulate a "scrolling image" effect,
    since some expressions may be too large to fit on the screen. Therefore a
    slider is needed, which can allow the user to "scroll" through an expression
    instead of scaling it down to the smallest size known to mankind
    """
    def __init__(self,
                 surface,
                 position,
                 window_width,
                 foreground_color = (96, 48, 48),
                 background_color = (48, 48, 48)):
        self.surface = surface
        self.position = position
        self.width = window_width
        self.height = surface.get_rect().h
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.slider_rect =[ self.position[0],
            self.position[1] + self.height + 10,
            int(self.width * 0.3), 10]
        self.clicked = False
        self.mousex = 0
        self.offset = 0
        self.scale_factor = \
            (self.surface.get_rect().w - self.width) / (self.width * 0.7)

    def get_height(self):
        return self.height + 10 + self.slider_rect[3]

    def move(self, x, y):
        self.slider_rect[0] += x
        self.slider_rect[1] += y
        self.position[0] += x
        self.position[1] += y

    def render(self, screen):
        """
        Draws the slider and a clipped portion of the full surface to the
        screen.
        """
        clipping_rect = (
            (self.slider_rect[0] - self.position[0]) * self.scale_factor,
            0,
            self.width,
            self.height
        )
        screen.blit(self.surface, self.position, clipping_rect)
        # now draw the bar and the background
        pygame.draw.rect(
            screen,
            self.background_color,
            [
                self.position[0],
                self.position[1] + self.height + 10,
                self.width,
                self.slider_rect[3]
            ],
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            self.foreground_color,
            self.slider_rect,
            border_radius = 8
        )

    def clickdown(self, pos):
        """
        Run when the mouse is clicked. Clickdown will test if the slider is
        being clicked, and set the appropriate variables if that is the case.
        """
        rect = pygame.rect.Rect(*self.slider_rect)
        if rect.collidepoint(pos):
            self.clicked = True
            self.mousex = pos[0]
            self.offset = self.slider_rect[0] - self.mousex

    def clickup(self):
        """
        If the mouse isn't clicking anymore, then the slider cannot be being
        clicked. It's that simple!
        """
        self.clicked = False

    def mousemotion(self, pos):
        """
        Movement is defined by the position of the mouse in relation to the
        position of the mouse when it first clicked the slider. Movement is
        calculated and the slider is also bound to stay within the slider
        box.
        """
        if self.clicked:
            self.slider_rect[0] = pos[0] + self.offset
            if self.slider_rect[0] < self.position[0]:
                self.slider_rect[0] = self.position[0]
            if self.slider_rect[0] > self.position[0] + self.width * 0.7:
                self.slider_rect[0] = self.position[0] + self.width * 0.7

