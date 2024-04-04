import tkinter as tk
import random
from Board import Board
from PuzzleSolver import a_star_search

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.size = 3
        self.nodes_explored = 0
        self.move_count = 0
        self.tiles = [[0 for _ in range(self.size)] for _ in range(self.size)]

        label_font = ('Arial', 12, 'bold')
        button_font = ('Helvetica', 16)
        frame_bg = '#f0f0f0'
        button_bg = '#e1e1e1'

        grid_frame = tk.Frame(master, bg=frame_bg)
        grid_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(grid_frame, text='', height=4, width=8, font=button_font, bg=button_bg,
                                   command=lambda row=i, col=j: self.move_tile(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

        status_frame = tk.Frame(master, bg=frame_bg)
        status_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.nodes_label = tk.Label(status_frame, text=f"Nodes explored: {self.nodes_explored}", font=label_font)
        self.nodes_label.pack(side="left", expand=True, fill="x")

        self.move_label = tk.Label(status_frame, text=f"Moves: {self.move_count}", font=label_font)
        self.move_label.pack(side="right", expand=True, fill="x")

        control_frame = tk.Frame(master, bg=frame_bg)
        control_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.shuffle_button = tk.Button(control_frame, text="Shuffle", command=self.shuffle, font=button_font, bg=button_bg)
        self.shuffle_button.pack(side="left", expand=True, fill="x", padx=5)

        self.solve_button = tk.Button(control_frame, text="Solve", command=self.solve, font=button_font, bg=button_bg)
        self.solve_button.pack(side="right", expand=True, fill="x", padx=5)
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
            new_state = self.tiles  
        
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
            board_state = board.get_state()
            self.move_label.config(text=f"Moves: {self.move_count}")
            self.update_board(board_state)
            self.master.update()
            self.master.after(500)
            self.master.update_idletasks() 
            self.move_count += 1



if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap('image.ico')
    root.title("Puzzle 8 pro Pepeho")
    app = PuzzleGUI(root)
    root.geometry("370x500") 
    root.mainloop()