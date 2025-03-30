import pygame

class TextInput:
    def __init__(self,
                 position,
                 width,
                 font,
                 font_size,
                 color,
                 submit_fn,
                 flavourtext = "Enter your answer here"):
        self.width = width
        self.font = font
        self.font_size = font_size
        self.font_width = self.font.size('a')[0]
        self.position = position
        self.colour = color
        self.line_colour = (230, 170, 30)
        self.flavourtext = flavourtext

        self.current_line_colour = self.line_colour
        self.current_colour      = self.colour
        self.target_colour       = (32, 32, 32)

        self.contents = ""
        self.content_surf = self.font.render("", True, (0, 0, 0))
        self.flavourtext_surf = self.font.render(
            flavourtext,
            True,
            [self.colour[0] - 64, self.colour[1] - 64, self.colour[2] - 64])
        self.cursor_position = 0
        self.last_cursor_position = 0
        self.window_pos = 0
        self.submit_fn = submit_fn

        self.active = False

    def render(self, screen):
        """
        Render draws both the cursor, the text input field and the text input
        "line" I guess
        """
        font_height = self.font.get_height()
        pygame.draw.line(
            screen,
            self.current_line_colour,
            [self.position[0], self.position[1] + font_height + 3],
            [self.position[0] + self.width, self.position[1] + font_height + 3],
            3
        )

        # draw the cursor
        cpos = self.cursor_position - self.window_pos
        pygame.draw.line(
            screen,
            self.current_line_colour,
            [self.position[0] + cpos * self.font_width,
                self.position[1]],
            [self.position[0] + cpos * self.font_width,
                self.position[1] + font_height - 3],
            3
        )

        if self.contents == "":
            screen.blit(self.flavourtext_surf, self.position)
        else:
            screen.blit(self.content_surf, self.position)

    def render_contents(self):
        """
        Does some dodgy string manipulation to get a "window" segment of the
        entire input string that is to be displayed.
        """
        # the input field is only so big, so we can only render at most a
        # window into the characters, so do that
        render = self.contents
        maxchars = int(self.width / self.font_width)
        if self.cursor_position > maxchars:
            self.window_pos = self.cursor_position - maxchars - 1

        render = self.contents[
            self.window_pos : (self.window_pos + maxchars + 1)
        ]
        self.content_surf = self.font.render(render, True, self.current_colour)

    def colour_interpolate(self, c, t, v):
        interp = [
            int(c[0] - (c[0] - t[0]) * v),
            int(c[1] - (c[1] - t[1]) * v),
            int(c[2] - (c[2] - t[2]) * v),
        ]
        return interp

    def set_opacity(self, c):
        """
        Set colour doesn't work how you would expect it to. Its more of an
        opacity slider, using the R value to determine how bright the
        respective elements of the textinput should be.
        """
        # opacity is a % color towards a target
        self.current_line_colour = self.colour_interpolate(
            self.line_colour, self.target_colour, c)
        self.current_colour = self.colour_interpolate(
            self.colour, self.target_colour, c)
        grayed = self.colour_interpolate([
            self.colour[0] - 64,
            self.colour[1] - 64,
            self.colour[2] - 64],
            self.target_colour, c)
        self.flavourtext_surf = self.font.render(
            self.flavourtext,
            True,
            grayed)
        self.render_contents()

    def reset(self):
        """
        Resets the input field, cursor position, etc.
        """
        self.contents = ""
        self.cursor_position = 0
        self.window_pos = 0

    def recieve_key_down(self, key, unicode):
        """
        Recieve key down takes a key code and its unicode character value. This
        is done so that we can decide a) what we want to do with the keycode
        and b) whether or not we should count it as a keystroke.
        """
        if key == pygame.K_BACKSPACE:
            if self.cursor_position > 0:
                self.contents = self.contents[:self.cursor_position - 1] + \
                    self.contents[self.cursor_position:]
                self.cursor_position -= 1
                self.render_contents()
        elif key == pygame.K_LEFT:
            if self.window_pos != 0 and (self.cursor_position == self.window_pos):
                self.window_pos -= 1
                print(self.window_pos)
            elif self.cursor_position > 0: self.cursor_position -= 1
            self.render_contents()
        elif key == pygame.K_RIGHT:
            if self.cursor_position < len(self.contents):
                self.cursor_position += 1
            self.render_contents()
        elif unicode != '':
            if self.active:
                if unicode == '\r' or unicode == '\n':
                    self.submit_fn(self.contents)
            if ord(unicode) >= 32 and ord(unicode) <= 126:
                self.contents = self.contents[:self.cursor_position] + unicode\
                    + self.contents[self.cursor_position:]
                self.cursor_position += 1

                # rerender the text
                self.render_contents()
