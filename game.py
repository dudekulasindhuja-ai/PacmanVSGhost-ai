# game.py

class Game:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        # Initial positions
        self.pacman = (0, 0)
        self.ghost = (rows - 1, cols - 1)
        self.goal = (rows - 1, 0)

        # Score
        self.score = 0

        # -------- WALLS (MAZE) -------- #
        self.walls = []
        
        # Simple vertical wall pattern
        for i in range(1, rows - 1):
            if i % 2 == 0:   # alternate rows
                self.walls.append((i, cols // 2))

        # -------- DOTS -------- #
        self.dots = [(i, j) for i in range(rows) for j in range(cols)
                     if (i, j) not in self.walls
                     and (i, j) != self.pacman
                     and (i, j) != self.ghost
                     and (i, j) != self.goal]

    # -------- MOVES -------- #
    def get_moves(self, pos):
        x, y = pos
        moves = []

        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (0 <= nx < self.rows and
                0 <= ny < self.cols and
                (nx, ny) not in self.walls):
                moves.append((nx, ny))

        return moves

    # -------- MOVE FUNCTIONS -------- #
    def move_pacman(self, new_pos):
        self.pacman = new_pos

    def move_ghost(self, new_pos):
        self.ghost = new_pos

    # -------- GAME CONDITIONS -------- #
    def is_ghost_win(self):
        return self.pacman == self.ghost

    def is_pacman_win(self):
        return self.pacman == self.goal

    def is_game_over(self):
        return self.is_pacman_win() or self.is_ghost_win()