import pygame
from PIL import Image

from emath import tex

DEFAULT_EQUATION_CACHE_DIR      = "cache/"
DEFAULT_EQUATION_CACHE_LOCATION = DEFAULT_EQUATION_CACHE_DIR + "cache.csv"
DEFAULT_PROPS = {
    'id' : 0
}

def get_top_pixel(pix, h, x):
    for i in range(h):
        if pix[x, i] != (255, 255, 255, 0):
            return i
    return 9999

def get_bottom_pixel(pix, h, x):
    for i in range(h - 1, 0, -1):
        if pix[x, i] != (255, 255, 255, 0):
            return i
    return 0

def get_left_pixel(pix, w, x):
    for i in range(w):
        if pix[i, x] != (255, 255, 255, 0):
            return i
    return 9999

def get_right_pixel(pix, w, x):
    for i in range(w - 1, 0, -1):
        if pix[i, x] != (255, 255, 255, 0):
            return i
    return 0

class EquationCache:
    """
    EquationCache: A place to store all of your equations!

    Because there are no easy ways to convert a LaTeX string into a pygame
    texture, a cache containing a bunch of generated images of LaTeX strings
    will be used. This is problematic since we need some way to store them and
    load them, so each one gets an ID and can be loaded as a pygame surface
    when needed.
    """
    def __init__(self):
        self.loaded_equations = {}
        self.props = {}

        self.load_equation_cache()

    def get(self, id):
        """
        Get an equation surface with an id
        """
        assert id in self.loaded_equations.keys()
        return self.loaded_equations[id]

    def load_equation(self, latex):
        """
        Converts a LaTeX equation into an image and loads it using pygame. It
        also caches the loaded image.
        The image is also cropped so that transparent blank space is minimized
        """
        filename = DEFAULT_EQUATION_CACHE_DIR + str(self.props['id']) + '.png'
        tex.render_latex_to_png(latex, filename)
        self.props['id'] += 1

        # load the cached equation as a pygame surface
        surface = pygame.image.load(filename)

        # because of how matplotlib works, we need to crop the image to only
        # contain the equation, since most of it will be empty
        im = Image.open(filename)
        pix = im.load()

        width, height = im.size
        top_pixel = 9999
        bottom_pixel = 0
        left_pixel = 9999
        right_pixel = 0

        for i in range(width):
            top_pixel = min(get_top_pixel(pix, height, i), top_pixel)
            bottom_pixel = max(get_bottom_pixel(pix, height, i), bottom_pixel)
        for i in range(height):
            left_pixel = min(get_left_pixel(pix, width, i), left_pixel)
            right_pixel = max(get_right_pixel(pix, width, i), right_pixel)
        print(left_pixel, right_pixel, top_pixel, bottom_pixel)

        # now that we have the top and bottom pixels, lets crop the image
        surface = surface.subsurface(
            (left_pixel,
             top_pixel,
             right_pixel - left_pixel + 1,
             bottom_pixel - top_pixel + 1))
        self.loaded_equations[self.props['id'] - 1] = surface

        return (surface, self.props['id'] - 1)

    def scale_equation(self, id, new_size):
        """
        Scales an equation surface to a new size and crops the image
        """
        assert id in self.loaded_equations.keys()
        scaled = pygame.transform.smoothscale(self.loaded_equations[id], new_size)
        self.loaded_equations[id] = scaled

        return scaled

    def unload_equation(self, id):
        """
        Unloads a pygame surface allocated to an ID
        """
        self.loaded_equations.pop(id, None)

    def unload_all(self):
        """
        Unloads all of the allocated pygame surfaces
        """
        for key in list(self.loaded_equations.keys()):
            self.loaded_equations.pop(key, None)

    def load_equation_cache(self):
        """
        Loads the equation cache from the cache save file. If there is no cache,
        then the cache is initialized to default values.
        """
        cache_info = ""
        try:
            with open(DEFAULT_EQUATION_CACHE_LOCATION, "r") as f:
                cache_info = f.read()
        except IOError:
            # the file doesn't exist, so lets make one
            with open(DEFAULT_EQUATION_CACHE_LOCATION, "w") as f:
                f.write('')
            self.props = DEFAULT_PROPS
            return

        cache_info.replace('\n', ',')
        cache_info = cache_info.split(',')
        for i in range(0, len(cache_info), 2):
            self.props[cache_info[i]] = int(cache_info[i + 1])

    def save_equation_cache(self):
        """
        Saves the default equation cache properties to a file
        """
        listified_cache = []
        for k, v in self.props.items():
            listified_cache += [str(k), str(v)]

        with open(DEFAULT_EQUATION_CACHE_LOCATION, "w") as f:
            f.write(','.join(listified_cache))
