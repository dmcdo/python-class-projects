import pygame


class MenuBarWidget:
    color_font = (0, 0, 0)  # color of the font
    color_button = (160, 160, 160) # color of the buttons not hovered, clicked
    color_clicked = (100, 100, 100)  # color of the buttons when clicked
    color_hover = (200, 200, 200)  # color of the buttons when hovered

    def __init__(self, screen, width, height, offset_x, offset_y, btn_labels):
        self._screen = screen
        self._btn_labels = btn_labels
        self._font = pygame.font.Font(None, 30)

        self._border = 10
        self._btns_count = len(self._btn_labels)
        self.resize(width, height, offset_x, offset_y)

    def draw_all(self):
        for i in range(len(self._buttons)):
            self.draw_button(i, MenuBarWidget.color_button)

    def draw_button(self, i, color):
        # render button
        pygame.draw.rect(self._screen, color, self._buttons[i])

        # render text
        text_surf = self._font.render(
            self._btn_labels[i], True, MenuBarWidget.color_font)
        text_rect = text_surf.get_rect()
        text_rect.centerx = self._buttons[i].centerx
        text_rect.centery = self._buttons[i].centery
        self._screen.blit(text_surf, text_rect)

    def locate(self, x, y):
        # determine which button (0, 1, ... n) was pressed
        for i, rect in enumerate(self._buttons):
            if rect.collidepoint((x, y)):
                return i

    def resize(self, width, height, offset_x, offset_y):
        self._width = width
        self._height = height
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._rect_width = width // self._btns_count - 2 * self._border
        self._rect_height = self._height - 2 * self._border

        # resize buttons
        self._buttons = []
        for i in range(len(self._btn_labels)):
            self._buttons.append(pygame.Rect(
                self._offset_x + i *
                (self._rect_width + 2 * self._border) + self._border,
                self._offset_y + self._border,
                self._rect_width,
                self._rect_height
            ))
