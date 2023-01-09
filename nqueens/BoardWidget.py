import pygame


class BoardWidget:
    colors = (0, 0, 0), (255, 255, 255)

    def __init__(self, screen, width, height, offset_x, offset_y, n):
        self._n = n
        self._screen = screen
        self._image_queen_unscaled = pygame.image.load('queen.png')
        self.resize(width, height, offset_x, offset_y)

    # determine which checkerboard square is at (mousex, mousey)
    def locate(self, mousex, mousey):
        x = (mousex - self._offset_x) // self._rect_width
        y = (mousey - self._offset_y) // self._rect_height

        if 0 <= x < self._n and 0 <= y < self._n:
            return (x, y)
        else:
            return None

    def draw_all(self, queen_locations=()):
        # Draw chekerboard pattens
        for x in range(self._n):
            for y in range(self._n):
                pygame.draw.rect(
                    self._screen,
                    BoardWidget.colors[(x % 2 + y % 2) % 2],
                    (
                        self._offset_x + x * self._rect_width,
                        self._offset_y + y * self._rect_height,
                        self._rect_width,
                        self._rect_height
                    )
                )

        # draw queens
        for queen in queen_locations:
            self.draw_queen(*queen)

    def draw_queen(self, x, y):
        centerx = self._offset_x + (x + 0.5) * self._rect_width
        centery = self._offset_y + (y + 0.5) * self._rect_height
        self._image_queen_rect.centerx = centerx
        self._image_queen_rect.centery = centery
        self._screen.blit(self._image_queen, self._image_queen_rect)
    
    def undraw_queen(self, x, y):
        # draw checkerboard square over queen
        pygame.draw.rect(
            self._screen,
            BoardWidget.colors[(x % 2 + y % 2) % 2],
            (
                self._offset_x + x * self._rect_width,
                self._offset_y + y * self._rect_height,
                self._rect_width,
                self._rect_height
            )
        )

    def resize(self, width, height, offset_x, offset_y):
        self._width = width
        self._height = height
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._rect_width = width // self._n
        self._rect_height = height // self._n

        queen_length = min(self._rect_width, self._rect_height)

        self._image_queen = pygame.transform.scale(
            self._image_queen_unscaled,
            (queen_length, queen_length)
        )
        self._image_queen_rect = self._image_queen.get_rect()
