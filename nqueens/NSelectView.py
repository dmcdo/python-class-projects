import pygame
from time import sleep, time
from EmptyView import EmptyView


class NSelectView(EmptyView):
    def __init__(self, screen, initial_n=8):
        super().__init__(screen)
        pygame.font.init()

        # Initialize fonts, text box, ok button, other text, cursor
        self._font1 = pygame.font.Font(None, 55)
        self._font2 = pygame.font.Font(None, 80)
        self._box = pygame.Rect(0, 0, 300, 100)
        self._btn = pygame.Rect(0, 0, 125, 100)
        self._cursor = pygame.Rect(0, 0, 3, 50)
        self._txt_ok = self._font2.render('OK', True, (0, 0, 0))
        self._txt_ok_rect = self._txt_ok.get_rect()
        self._txt_enter = self._font1.render('Enter value for n below',
                                             True, (255, 255, 255))
        self._txt_enter_rect = self._txt_enter.get_rect()
        self._txt_n_str = str(initial_n)
        self._txt_n = self._font2.render(
            self._txt_n_str, True, (255, 255, 255))
        self._txt_n_rect = self._txt_n.get_rect()

        # Is the ok button down?
        self._btn_down = False

    def resize(self):
        super().resize(575, 500)

        # Reallign view components to new size
        self._box.centerx = self._width // 2 - self._btn.width // 2 - 10
        self._box.centery = self._height // 2
        self._btn.centerx = self._width // 2 + self._box.width // 2 + 10
        self._btn.centery = self._height // 2
        self._txt_ok_rect.centerx = self._btn.left + self._btn.width // 2
        self._txt_ok_rect.centery = self._height // 2
        self._txt_enter_rect.centerx = self._width // 2
        self._txt_enter_rect.centery = self._height // 2 - 80
        self._txt_n_rect.left = self._box.left + 20
        self._txt_n_rect.centery = self._height // 2
        self._cursor.left = self._txt_n_rect.right + 6
        self._cursor.centery = self._height // 2

        self.draw_all()

    def draw_all(self):
        super().draw_all()

        self._ok_btn_draw((255, 255, 255))
        pygame.draw.rect(self._screen, (255, 255, 255),
                         self._box, width=3)  # text box
        pygame.draw.rect(self._screen, self._get_cursor_color(),
                         self._cursor)  # cursor
        self._screen.blit(self._txt_enter, self._txt_enter_rect)  # 'Enter n'
        self._screen.blit(self._txt_n, self._txt_n_rect)  # user-entered number

    def _event_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.WINDOWRESIZED:
                    self.resize()
                elif event.type == pygame.KEYDOWN:
                    # In case Enter/Return in pressed
                    if n := self._keydown(event.key):
                        return n
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # if the ok button is now down
                    if self._btn.collidepoint(pygame.mouse.get_pos()):
                        self._btn_down = True
                        self._ok_btn_draw((175, 175, 175))
                elif event.type == pygame.MOUSEBUTTONUP:
                    # if the ok button is now up
                    if self._btn.collidepoint(pygame.mouse.get_pos()):
                        if len(self._txt_n_str):
                            return int(self._txt_n_str)  # terminate, return n
                    self._btn_down = False
                    self._ok_btn_draw((220, 220, 220))
                elif event.type == pygame.MOUSEMOTION:
                    if self._btn_down:
                        pass
                    # elif button being hovered over
                    elif self._btn.collidepoint(pygame.mouse.get_pos()):
                        self._ok_btn_draw((220, 220, 220))
                    else:
                        self._ok_btn_draw((255, 255, 255))

            pygame.draw.rect(
                self._screen, self._get_cursor_color(), self._cursor)
            pygame.display.flip()
            sleep(1/30)

    def _keydown(self, key):
        if key == pygame.K_RETURN:
            if len(self._txt_n_str):
                return int(self._txt_n_str) # tell event loop to terminate w/ n
        elif key == pygame.K_BACKSPACE:
            if len(self._txt_n_str):
                self._update_txt_n(self._txt_n_str[:-1])
        elif key == pygame.K_0:
            if len(self._txt_n_str) == 1: # user cannot enter just 0
                self._update_txt_n(self._txt_n_str + '0')
        elif key in {pygame.K_1, pygame.K_2, pygame.K_3,
                     pygame.K_4, pygame.K_5, pygame.K_6,
                     pygame.K_7, pygame.K_8, pygame.K_9}:
            if len(self._txt_n_str) < 2:
                self._update_txt_n(self._txt_n_str + pygame.key.name(key))

    def _ok_btn_draw(self, color):
        pygame.draw.rect(self._screen, color, self._btn)
        self._screen.blit(self._txt_ok, self._txt_ok_rect)

    # update text in text box to be s
    def _update_txt_n(self, s):
        self._txt_n_str = s
        self._txt_n = self._font2.render(
            self._txt_n_str, True, (255, 255, 255))
        self._txt_n_rect = self._txt_n.get_rect()
        self._screen.fill((0, 0, 0))
        self.resize()
        self.draw_all()

    def _get_cursor_color(self):
        if int(time() * 10) % 10 > 5:
            return (255, 255, 255)
        else:
            return (0, 0, 0)
