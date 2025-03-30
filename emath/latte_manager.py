import pygame

from emath.question_manager import DifferentialQuestionManager
from emath.menu import Menu
from emath.text import Text
from emath.background import Background
from emath.selection_arrows import SelectionArrows

class LatteManager:
    """
    Here it is: The source of everything
    Latte manager is the underlying core of lattice, and handles all of the
    menus and loaded question managers
    """
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()

        self.font = pygame.font.Font('res/robotomono.ttf', 28)
        self.bigfont = pygame.font.Font('res/robotomono.ttf', 200)

        self.do_question = False

        self.init_big_font()

        self.load_question_managers()

        self.current_question_manager = \
            self.loaded_question_managers["differential"]

        self.load_menus()
        self.load_background()


    def init_big_font(self):
        """
        This algorithm is awful, since pygame wont allow you to change the font
        size of an already existing font object. :(
        """
        # we want the font size that at least covers this area vertically
        defined_area = 0.15 * self.height
        size = 20
        while self.bigfont.get_height() < defined_area:
            self.bigfont = pygame.font.Font('res/robotomono.ttf', size)
            size += 1

    def load_background(self):
        """
        What I'm going for with this is the background looking thing from
        sebastian lague's youtube videos. It looks really cool imo
        """
        self.background = Background(60, self.width, self.height)

    def load_question_managers(self):
        """
        A question manager is an object that manages asking questions to the
        user. As of now the only question manager is the differential equation
        question manager, but I will probably add more later.
        """
        self.loaded_question_managers = {
            "differential" : DifferentialQuestionManager(self.screen, self.font)
        }

    def load_main_menu(self):
        """
        Creates a main menu object
        """
        main_menu = Menu(self.screen, self.width, self.height)

        main_text = Text("Lattice", self.bigfont, [0, self.height * 0.3])
        main_text.position[0] = (self.width - main_text.get_width()) / 2
        diff_text = Text(
            "Differentiation Practice",
            self.font, [0, self.height * 0.3 + self.bigfont.get_height() + 10])
        diff_text.position[0] = (self.width - diff_text.get_width()) / 2
        difficulty_text_1 = Text(
            "Increase Difficulty",
            self.font,
            [0, self.height * 0.3 + self.bigfont.get_height() + 10 + \
                self.font.get_height()])
        difficulty_text_1.position[0] = \
            (self.width - difficulty_text_1.get_width()) / 2
        difficulty_text_2 = Text(
            "Decrease Difficulty",
            self.font,
            [0, self.height * 0.3 + self.bigfont.get_height() + 10 + \
                self.font.get_height() * 2])
        difficulty_text_2.position[0] = \
            (self.width - difficulty_text_1.get_width()) / 2
        difficulty_value = Text(
            "Difficulty: {:02d}".\
                format(self.current_question_manager.difficulty_level),
            self.font, [0, self.height * 0.9])
        difficulty_value.position[0] = \
            (self.width - difficulty_value.get_width()) / 2

        select_arrows = SelectionArrows(
            [0, diff_text.position[1]],
            diff_text.get_width() + 50,
            [0, 0, 0],
            3,
            self.font,
            self.on_selected_main_menu_option
        )
        select_arrows.position[0] = (self.width - (diff_text.get_width() + 50) \
            - select_arrows.arrow_size) / 2

        main_menu.add_element("lattice", main_text)
        main_menu.add_element("diff", diff_text)
        main_menu.add_element("sel", select_arrows)
        main_menu.add_element("diff_inc", difficulty_text_1)
        main_menu.add_element("diff_dec", difficulty_text_2)
        main_menu.add_element("diff_val", difficulty_value)
        main_menu.add_element("ver", Text("v0.0.01a", self.font, [10, 10]))

        return main_menu

    def load_menus(self):
        self.menus = {
            "main" : self.load_main_menu()
        }

    def begin_questions(self):
        self.menus['main'].active = False
        self.do_question = True
        self.current_question_manager.generate_question()

    def on_selected_main_menu_option(self, option):
        if option == 0:
            self.menus['main'].transition(
                240,
                [ 32, 32, 32 ],
                self.begin_questions
            )
        elif option == 1:
            if self.current_question_manager.difficulty_level < 12:
                self.current_question_manager.difficulty_level += 1
            self.menus['main'].get('diff_val').text = "Difficulty: {:02d}" \
                .format(self.current_question_manager.difficulty_level)
        elif option == 2:
            if self.current_question_manager.difficulty_level > 3:
                self.current_question_manager.difficulty_level -= 1
            self.menus['main'].get('diff_val').text = "Difficulty: {:02d}" \
                .format(self.current_question_manager.difficulty_level)
        print(option)

    def update(self, events, delta):
        """
        Update updates literally everything per frame
        """
        if self.do_question:
            self.current_question_manager.update(events, delta)
        else:
            self.menus["main"].update(events, delta)
            self.background.update(events, delta)

    def render(self):
        """
        Renders the active contexts
        """
        if self.do_question:
            self.current_question_manager.render()
        else:
            self.background.render(self.screen)
            self.menus["main"].render()

    def close(self):
        self.current_question_manager\
            .renderer\
            .equation_cache\
            .save_equation_cache()
