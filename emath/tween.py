import pygame
import math

MOVE_NONE   = 0
MOVE_SIN    = 1

TWEEN_ID = 0

class Tween:
    """
    Tween is a wrapper for objects that implement the move(), get_colour()
    and render() methods. Tween itself stands for inbet-Tween, allowing for
    smooth movements of elements on the screen.
    """
    def __init__(self, obj):
        global TWEEN_ID
        self.obj = obj
        self.target_frames = 0
        self.current_frame = 0
        self.frame_factor = 0

        self.target = []
        self.delta = []

        self.move_type = MOVE_NONE
        self.moving = False

        self.waiting = False
        self.wait_fn = None

        self.colour_change = False

        self.id = TWEEN_ID
        TWEEN_ID += 1

    def render(self, screen):
        self.obj.render(screen)

    def wait_then(self, fn, frames):
        """
        Wait then waits a number of frames before executing a function by
        passing itself to the function.
        """
        self.target_frames = frames
        self.current_frames = 0
        self.wait_fn = fn
        self.waiting = True

    def move_sin(self, delta_x, delta_y, frames):
        """
        Moves an object according to a sin curve to its destination.
        Look dont't ask me how I figured all of the maths out just know some
        dodgy integrations and summations were used.
        """
        self.frame_factor = math.pi / (2 * frames)
        self.target_frames = frames
        self.current_frame = 0
        self.moving = True
        self.move_type = MOVE_SIN

        # calculating delta time
        self.target = [delta_x, delta_y]
        self.delta = [0, 0]

    def change_color(self, target, frames):
        self.colour_change = True
        self.current_frame = 0
        self.target_frames = frames

        obj_col = self.obj.get_colour()
        self.delta = [
            (target[0] - obj_col[0]) / frames,
            (target[1] - obj_col[1]) / frames,
            (target[2] - obj_col[2]) / frames
        ]

    def update(self):
        if self.moving:
            if self.move_type == MOVE_SIN:
                if self.current_frame == self.target_frames:
                    self.moving = False
                    return
                self.obj.move(
                    math.sin(self.current_frame * self.frame_factor) * \
                        self.target[0] - self.delta[0],
                    math.sin(self.current_frame * self.frame_factor) * \
                        self.target[1] - self.delta[1],
                )
                self.delta = [
                    math.sin(self.current_frame * self.frame_factor) * \
                        self.target[0],
                    math.sin(self.current_frame * self.frame_factor) * \
                        self.target[1]
                ]
            self.current_frame += 1
        elif self.waiting:
            if self.current_frame == self.target_frames:
                self.wait_fn(self)
                self.waiting = False
            self.current_frame += 1
        elif self.colour_change:
            if self.current_frame == self.target_frames:
                self.colour_change = False
            self.obj.colour[0] += self.delta[0]
            self.obj.colour[1] += self.delta[1]
            self.obj.colour[2] += self.delta[2]
            self.current_frame += 1
