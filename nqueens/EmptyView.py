from pygame.display import set_mode
from pygame.constants import RESIZABLE


# Base class for NSelectView and GameView
class EmptyView():
    def __init__(self, screen):
        self._screen = screen
        self._width, self._height = screen.get_size()

    # Blocking function that allows the view to take over the _screen
    def exec(self):
        self.resize()
        self.draw_all()
        return self._event_loop()

    def resize(self, min_width, min_height, set_mode_flags=RESIZABLE):
        self._width, self._height = self._screen.get_size()
        if self._width < min_width:
            self._width = min_width
        if self._height < min_height:
            self._height = min_height
        self._screen = set_mode((self._width, self._height), set_mode_flags)

    def draw_all(self):
        self._screen.fill((0, 0, 0))

    # Blocks until otherwise terminated from within
    def _event_loop(self):
        pass
