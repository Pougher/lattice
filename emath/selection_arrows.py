import pygame

class SelectionArrows:
    def __init__(self, position, width, colour, count, font, select_fn):
        self.colour = colour
        self.position = position
        self.width = width

        self.active = True

        self.option = 0
        self.distance_between_options = font.get_height()
        self.count = count

        self.arrow_left = font.render('>', True, self.colour)
        self.arrow_right = font.render('<', True, self.colour)

        self.arrow_size = font.size('>')[0]

        self.select_fn = select_fn

    def render(self, screen):
        """
        Draws the two selection arrows a distance apart
        """
        screen.blit(self.arrow_left, [
            self.position[0],
            self.position[1] + self.option * self.distance_between_options])
        screen.blit(self.arrow_right, [
            self.position[0] + self.width,
            self.position[1] + self.option * self.distance_between_options])

    def process_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.option > 0: self.option -= 1
                elif event.key == pygame.K_DOWN:
                    if self.option < self.count - 1: self.option += 1
                elif event.key == pygame.K_SPACE:
                    self.select_fn(self.option)

    def update(self, events, delta):
        if self.active: self.process_events(events)
