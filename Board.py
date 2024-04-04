class Board:
    def __init__(self, tiles):
        self.tiles = [row[:] for row in tiles]
        self.n = len(tiles)
        self.blank_row, self.blank_col = self._find_blank()

    def __str__(self):
        return f'\n'.join(' '.join(str(tile) for tile in row) for row in self.tiles)
    
    def __eq__(self, other):
        if not isinstance(other, Board) or self.n != other.n:
            return False
        return self.tiles == other.tiles

    def _find_blank(self):
        for row in range(self.n):
            for col in range(self.n):
                if self.tiles[row][col] == 0:
                    return row, col
        return -1, -1 # pokud je board validni, nemelo by se to stat

    def get_state(self):
        return self.tiles

    def neighbors(self):
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Doprava, Dolu, Doleva, Nahoru
        for dr, dc in directions:
            nr, nc = self.blank_row + dr, self.blank_col + dc
            if 0 <= nr < self.n and 0 <= nc < self.n:
                new_tiles = [row[:] for row in self.tiles]  # Kopie
                new_tiles[self.blank_row][self.blank_col], new_tiles[nr][nc] = new_tiles[nr][nc], new_tiles[self.blank_row][self.blank_col]
                moves.append(Board(new_tiles))
        return moves
        return moves

    def isGoal(self):
        goal = 1
        for row in range(self.n):
            for col in range(self.n):
                if row == self.n - 1 and col == self.n - 1:
                    return self.tiles[row][col] == 0
                if self.tiles[row][col] != goal:
                    return False
                goal += 1
        return True
    
    def hamming(self):
        distance = 0
        goal = 1
        for row in range(self.n):
            for col in range(self.n):
                if self.tiles[row][col] != 0 and self.tiles[row][col] != goal:
                    distance += 1
                goal += 1
        return distance
    
    def manhattan(self):
        distance = 0
        for row in range(self.n):
            for col in range(self.n):
                tile = self.tiles[row][col]
                if tile != 0:
                    goal_row, goal_col = (tile - 1) // self.n, (tile - 1) % self.n
                    distance += abs(row - goal_row) + abs(col - goal_col)
        return distance
            
    def _inversion_count(self):
        flat_tiles = [tile for row in self.tiles for tile in row if tile != 0]
        inversions = 0
        for i in range(len(flat_tiles)):
            for j in range(i + 1, len(flat_tiles)):
                if flat_tiles[i] > flat_tiles[j]:
                    inversions += 1
        return inversions

    def isSolvable(self):
        inv_count = self._inversion_count()
        # pro puzzle 8 velikost boardu je licha --> zjistime jestli je inversion sudy
        return inv_count % 2 == 0


