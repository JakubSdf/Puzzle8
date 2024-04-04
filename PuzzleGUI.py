import tkinter as tk
import random
from Board import Board
from PuzzleSolver import a_star_search

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Puzzle 8")
        self.size = 3
        self.tiles = [[0] * self.size for _ in range(self.size)] # Placeholder pro stav puzzle
        self.nodes_explored = 0
        self.move_count = 1
        self.nodes_label = tk.Label(master, text=f"Nodes explored: {self.nodes_explored}")
        self.nodes_label.grid(row=self.size + 3, column=0, columnspan=self.size, sticky="ew")

        self.move_label = tk.Label(master, text=f"Moves: {self.move_count - 1}")
        self.move_label.grid(row=self.size + 2, column=0, columnspan=self.size, sticky="ew")
    
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(master, text='', height=4, width=8,
                                   command=lambda row=i, col=j: self.move_tile(row, col))
                button.grid(row = i, column = j)
                self.buttons[i][j] = button
        
        control_frame = tk.Frame(master)
        control_frame.grid(row=self.size, column=0, columnspan=self.size, sticky="ew")

        self.shuffle_button = tk.Button(control_frame, text="Shuffle", command=self.shuffle)
        self.shuffle_button.pack(side="left", expand=True, fill="x")

        self.solve_button = tk.Button(control_frame, text="Solve", command=self.solve)
        self.solve_button.pack(side="right", expand=True, fill="x")

        self.init_board()

    def init_board(self):
        num = 1
        for i in range(self.size):
            for j in range(self.size):
                if num >= self.size * self.size:
                    self.tiles[i][j] = 0
                    self.buttons[i][j]['text'] = ''
                else:
                    self.tiles[i][j] = num
                    self.buttons[i][j]['text'] = str(num)
                num += 1

    def move_tile(self, row, col):
        if self.is_neighbor_blank(row, col):
            blank_row, blank_col = self.find_blank()
            self.swap_tiles(row, col, blank_row, blank_col)
            self.update_board()
            self.move_count += 1
            self.move_label.config(text=f"Moves: {self.move_count}")


    def is_neighbor_blank(self, row, col):
        blank_row, blank_col = self.find_blank()
        return abs(blank_row - row) + abs(blank_col - col) == 1

    def shuffle(self, moves=100):
        for _ in range(moves):
            blank_row, blank_col = self.find_blank()
            neighbors = self.get_blank_neighbors(blank_row, blank_col)
            if neighbors:
                chosen_row, chosen_col = random.choice(neighbors)
                self.swap_tiles(blank_row, blank_col, chosen_row, chosen_col)
            self.update_board()
            self.move_count = 0
            self.move_label.config(text=f"Moves: {self.move_count}")
            self.nodes_explored = 0
            self.nodes_label.config(text=f"Nodes explored: {self.nodes_explored}")


    def find_blank(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.tiles[i][j] == 0:
                    return i, j
        return -1, -1 # Nemelo by nastat pokud je puzzle validni
    
    def get_blank_neighbors(self, row, col):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Nahoru, Dolu, Doleva, Doprava
        for  dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.size and 0 <= c < self.size:
                neighbors.append((r, c))
        return neighbors

    def swap_tiles(self, row1, col1, row2, col2):
        self.tiles[row1][col1], self.tiles[row2][col2] = self.tiles[row2][col2], self.tiles[row1][col1]

    def update_board(self, new_state=None):
        if new_state is None:
            new_state = self.tiles  # Assuming self.tiles holds the current state
        
        for i in range(self.size):
            for j in range(self.size):
                tile_value = new_state[i][j]
                button_text = '' if tile_value == 0 else str(tile_value)
                self.buttons[i][j]['text'] = button_text

    def solve(self):
        initial_state = [[int(self.buttons[i][j]['text']) if self.buttons[i][j]['text'] else 0
                              for j in range(self.size)] for i in range(self.size)]
        initial_board = Board(initial_state)

        # A* hledaci algoritmus
        solution, nodes_explored = a_star_search(initial_board)
        self.nodes_explored = nodes_explored  # Update nodes explored count
        self.nodes_label.config(text=f"Nodes explored: {self.nodes_explored}")

        if solution:
            self.animate_solution(solution)
        else:
            print("Nenalezeno zadne reseni")

    def animate_solution(self, solution):
        for board in solution:
            self.started = True
            board_state = board.get_state()  # Adjust based on your Board class
            self.move_label.config(text=f"Moves: {self.move_count}")
            self.update_board(board_state)
            self.master.update()
            self.master.after(500)
            self.master.update_idletasks()  # Ensure the GUI updates are drawn
            self.move_count += 1



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = PuzzleGUI(root)
    root.mainloop()
