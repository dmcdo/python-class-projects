import pygame
from time import sleep
from EmptyView import EmptyView
from MenuBarWidget import MenuBarWidget
from BoardWidget import BoardWidget
from GameLogic import GameLogic


# Shows game portion of the N Queens Game
# Contains the game board and menu board
class GameView(EmptyView):
    ########
    # init #
    ########
    def __init__(self, screen, n, timely_solve_limit=8):
        super().__init__(screen)
        self._n = n

        # The program will not attempt to determine whether a given board
        # is solvable for n remaining queens larger than this value
        # You may want to lower this if the game becomes laggy
        self._timely_solve_limit = timely_solve_limit

        # Initializations
        pygame.font.init()
        pygame.mixer.init()

        # Sounds
        self._sound_failure = pygame.mixer.Sound('failure.wav')
        self._sound_success = pygame.mixer.Sound('success.wav')

        # Misc.
        self._menubar_height = 60
        self._infotext_height = 25
        self._button_down = None
        self._button_hovered = None
        self._exit_to_menu_now = False
        self._unsolvable = False

        # Game Logic
        self._logic = GameLogic(self._n)

        # Initialize Widgets
        self._menubar = MenuBarWidget(
            self._screen,
            self._width,
            self._menubar_height,
            0,
            0,
            ('Restart', 'Menu', 'Solve', 'Hint', 'Undo')
        )
        self._board = BoardWidget(
            self._screen,
            self._width,
            self._height - self._menubar_height - self._infotext_height,
            0,
            self._menubar_height + self._infotext_height,
            self._n
        )

    #######################
    # EmptyView Overrides #
    #######################
    def resize(self):
        super().resize(575, 500)

        self._board.resize(
            self._width,
            self._height - self._menubar_height - self._infotext_height,
            0,
            self._menubar_height + self._infotext_height
        )
        self._menubar.resize(self._width, self._menubar_height, 0, 0)
        self.draw_all()

    def draw_all(self):
        super().draw_all()

        self._board.draw_all(self._logic.get_queen_locations())
        self._menubar.draw_all()
        self._set_infotext()

    def _event_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.WINDOWRESIZED:
                    self.resize()
                elif event.type == pygame.MOUSEMOTION:
                    self._mousemotion(*pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._mousedown(*pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP:
                    self._mouseup(*pygame.mouse.get_pos())

            if self._exit_to_menu_now:
                return

            pygame.display.flip()
            sleep(1/30)  # Give the CPU a break

    ###########################
    # Menu Bar Button Methods #
    ###########################
    def restart(self):
        while self.undo(_set_infotext=False):
            pass
        self._unsolvable = False
        self._set_infotext()

    def menu(self):
        self._exit_to_menu_now = True

    def solve(self):
        # if solution exists
        if not self._unsolvable and (solution := self._logic.find_solution_current()):
            # place all the queens in the solution that haven't already been placed
            for x, y in solution[len(self._logic.get_queen_locations()):]:
                self._logic.push_queen(x, y)
                self._board.draw_queen(x, y)
                pygame.mixer.Sound.play(self._sound_success)
                pygame.display.flip()
                sleep(1/3)
            self._set_infotext()
        else:
            self._unsolvable = True
            self._set_infotext()

    def hint(self):
        # Attempt to find solution and place some queen from the solution
        if len(self._logic.get_queen_locations()) < self._n and not self._unsolvable:
            if solution := self._logic.find_solution_current():
                x, y = solution[len(self._logic.get_queen_locations())]
                self.place_queen(x, y)
            else:
                self._unsolvable = True
                self._set_infotext()

    def undo(self, _set_infotext=True):
        try:
            if coord := self._logic.pop_queen():
                self._unsolvable = False
                self._board.undraw_queen(*coord)
                if _set_infotext:
                    self._set_infotext()
                return coord
        except IndexError:
            pass  # nothing to pop

    #################
    # Event methods #
    #################
    def _mousemotion(self, x, y):
        # Show if mouse is hovering over a menu bar button
        if self._button_down is None:
            i = self._menubar.locate(x, y)
            if self._button_hovered is not None:
                if i != self._button_hovered:
                    self._menubar.draw_button(self._button_hovered,
                                              MenuBarWidget.color_button)
                    self._button_hovered = None
            if i is not None:
                self._menubar.draw_button(i, MenuBarWidget.color_hover)
                self._button_hovered = i

    def _mousedown(self, x, y):
        if board_pos := self._board.locate(x, y):  # queen placed
            self.place_queen(*board_pos)
        elif (button_clicked := self._menubar.locate(x, y)) is not None:  # menu bar button pressed
            self._button_down = button_clicked
            self._menubar.draw_button(
                button_clicked, MenuBarWidget.color_clicked)
            pygame.display.flip()

    def _mouseup(self, x, y):
        if self._button_down is not None:  # menu bar button pressed
            button_actions = (
                self.restart,
                self.menu,
                self.solve,
                self.hint,
                self.undo
            )

            self._menubar.draw_button(
                self._button_down, MenuBarWidget.color_hover)
            button_actions[self._button_down]()
            self._button_down = None

    #########
    # Misc. #
    #########
    def _set_infotext(self):
        # Clear text area
        pygame.draw.rect(
            self._screen,
            (0, 0, 0),
            (
                0,
                self._menubar_height,
                self._width,
                self._infotext_height
            )
        )

        # determine text to write
        queen_locations = self._logic.get_queen_locations()
        if self._unsolvable:
            infotext = 'The current board cannot be solved.'
        elif self._n == len(queen_locations):
            infotext = 'Congratulations! You win!'
        elif self._n - len(queen_locations) > self._timely_solve_limit:
            infotext = 'Cannot easily determine if the current board is solvable.'
        elif self._logic.find_solution_current():
            infotext = 'The current board can be solved.'
        else:
            infotext = 'The current board cannot be solved.'

        # write the text
        font = pygame.font.Font(None, 30)
        surf = font.render(infotext, True, (255, 255, 255))
        self._screen.blit(surf, (
            self._menubar._border,
            self._menubar_height
        ))

    def place_queen(self, x, y):
        if self._logic.can_place_at(x, y):
            pygame.mixer.Sound.play(self._sound_success)
            self._logic.push_queen(x, y)
            self._board.draw_queen(x, y)
        else:
            pygame.mixer.Sound.play(self._sound_failure)

        self._set_infotext()
