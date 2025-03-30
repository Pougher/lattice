import pygame
import math

MOVE_NONE   = 0
MOVE_SIN    = 1

TWEEN_ID = 0

# NOTE:
# This method of doing things is inefficient. I will extend tween later using
# list objects and separate classes. For now this works.

class Tween:
    """
    Tween is a wrapper for objects that implement the following (if you arent
    using every functioin of tween, some of these don't have to be implemented):
    - move()
    - get_colour()
    - set_colour()
    - set_opacity()
    - render()
    Tween itself stands for inbe-Tween, allowing for smooth movements of
    elements on the screen.
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
        self.fading = False

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
        self.current_frame = 0
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
        """
        Interpolates between a colour and another colour over a period of time
        """
        self.colour_change = True
        self.current_frame = 0
        self.target_frames = frames

        obj_col = self.obj.get_colour()
        self.delta = [
            (target[0] - obj_col[0]) / frames,
            (target[1] - obj_col[1]) / frames,
            (target[2] - obj_col[2]) / frames
        ]

    def fade(self, frames):
        """
        Fades a colour to the object's background colour over a set nunber of
        frames
        """
        self.fading = True
        self.current_frame = 0
        self.target_frames = int(math.fabs(frames))

        if frames < 0:
            self.delta = -1.0 / int(math.fabs(frames))
        else:
            self.delta = 1.0 / frames

    def in_transition(self):
        """
        Use this method to find out if a tween is still in a transitionary
        phase
        """
        return \
            (self.moving or self.waiting or self.fading or self.colour_change)

    def update(self):
        """
        Performs the currently assigned action. This is like the worst way to
        do this. A much better way would be a queue, but I will do that later.
        Should be really easy to implement.
        """
        if self.moving:
            if self.move_type == MOVE_SIN:
                if self.current_frame == self.target_frames:
                    self.moving = False
                    self.move_type = MOVE_NONE
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
                return
            self.current_frame += 1
        elif self.colour_change:
            if self.current_frame == self.target_frames:
                self.colour_change = False
                print("FINISHED: ", self.current_frame, self.target_frames, self.obj)
                return
            self.obj.colour[0] += self.delta[0]
            self.obj.colour[1] += self.delta[1]
            self.obj.colour[2] += self.delta[2]
            self.current_frame += 1
        elif self.fading:
            if self.current_frame == self.target_frames:
                print("FINISHED: ", self.current_frame, self.target_frames, self.obj)
                self.fading = False
                return

            if self.delta < 0:
                self.obj.set_opacity(math.fabs(self.delta) * self.current_frame)
            else:
                self.obj.set_opacity(1 - self.delta * self.current_frame)
            self.current_frame += 1
