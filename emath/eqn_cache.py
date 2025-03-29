import pygame

from emath import tex

DEFAULT_EQUATION_CACHE_DIR      = "cache/"
DEFAULT_EQUATION_CACHE_LOCATION = DEFAULT_EQUATION_CACHE_DIR + "cache.csv"
DEFAULT_PROPS = {
    'id' : 0
}

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
        """
        filename = DEFAULT_EQUATION_CACHE_DIR + str(self.props['id']) + '.png'
        tex.render_latex_to_png(latex, filename)
        self.props['id'] += 1

        # load the cached equation as a pygame surface
        surface = pygame.image.load(filename)
        self.loaded_equations[self.props['id'] - 1] = surface

        return (surface, self.props['id'] - 1)

    def scale_equation(self, id, new_size):
        """
        Scales an equation surface to a new size
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
