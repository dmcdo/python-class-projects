class GameLogic:
    def __init__(self, n):
        if n <= 0:
            raise ValueError()

        self._n = n
        self._queen_stack = []

        # The grid system
        # A queen can only occupy one row, col, diag, so this is all that needs to be remembered
        self._row_has_queen = [False] * n
        self._col_has_queen = [False] * n
        self._backward_diag_has_queen = {}
        self._forward_diag_has_queen = {}
        for i in range(-n + 1, n):
            self._backward_diag_has_queen[i] = False
            self._forward_diag_has_queen[i] = False

    def get_queen_locations(self):
        return tuple(self._queen_stack)

    def can_place_at(self, x, y):
        return \
            not self._col_has_queen[x] and \
            not self._row_has_queen[y] and \
            not self._backward_diag_has_queen[x - y] and \
            not self._forward_diag_has_queen[y - (self._n - 1 - x)]

    def push_queen(self, x, y):
        if not self.can_place_at(x, y):
            raise IndexError(f'Invalid Position ({x}, {y})')

        self._queen_stack.append((x, y))
        self._col_has_queen[x] = True
        self._row_has_queen[y] = True
        self._backward_diag_has_queen[x - y] = True
        self._forward_diag_has_queen[y - (self._n - 1 - x)] = True

    def pop_queen(self):
        try:
            x, y = self._queen_stack.pop()
        except IndexError:
            return None

        self._col_has_queen[x] = False
        self._row_has_queen[y] = False
        self._backward_diag_has_queen[x - y] = False
        self._forward_diag_has_queen[y - (self._n - 1 - x)] = False
        return x, y

    # Find a solution with the queens in their current position (no side effects)
    # If there is no solution return None, otherwise, a tuple containing the solution
    def find_solution_current(self):
        queens_placed = len(self._queen_stack)

        solution = self.solve_current()
        if solution:
            while len(self._queen_stack) > queens_placed:
                self.pop_queen()
            return solution
        else:
            return None

    # Find a solution with the queens in their current position (yes side effects)
    # If there is no solution return None, otherwise, a tuple containing the solution
    def solve_current(self, _startcol=0):
        if len(self._queen_stack) == self._n:
            return tuple(self._queen_stack)

        for x in range(_startcol, self._n):
            if self._col_has_queen[x]:
                continue

            for y in range(self._n):
                if self.can_place_at(x, y):
                    self.push_queen(x, y)

                    solution = self.solve_current(_startcol=x + 1)
                    if solution is not None:
                        return solution
                    else:
                        self.pop_queen()
