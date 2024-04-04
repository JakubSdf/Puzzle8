from Board import Board
import heapq # Pro operace prioritnich front

class Node:
    def __init__(self, board, parent=None, g=0):
        self.board = board
        self.parent = parent
        self.g = g # Cost od zacatku do aktualniho Node
        self.h = board.manhattan() # Heuristick cost od aktualniho Node k cili
        self.f = g + self.h # Totalni cost

    def __lt__(self, other):
        return self.f < other.f
    
def a_star_search(initial_board):
    start_node = Node(initial_board, None, 0)
    open_set = []
    heapq.heappush(open_set, (start_node.f, start_node))

    visited = set()

    while open_set:
        current_node = heapq.heappop(open_set)[1]

        if current_node.board.isGoal():
            return reconstruct_path(current_node)
        
        visited.add(str(current_node.board))
        
        for neighbor in current_node.board.neighbors():
            if str(neighbor) in visited:
                continue
            neighbor_node = Node(neighbor, current_node, current_node.g + 1)
            
            heapq.heappush(open_set, (neighbor_node.f, neighbor_node))

    return None

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.board)
        node = node.parent
    return path[::-1] # vrati obracenou cestu
        
'''

initial_states = [
    ([[1, 2, 3], [4, 5, 6], [7, 0, 8]], "Easy"),
    ([[1, 2, 3], [5, 0, 6], [4, 7, 8]], "Medium"),
    ([[2, 8, 1], [0, 4, 3], [7, 6, 5]], "Hard"),
    ([[8, 6, 7], [2, 5, 4], [3, 0, 1]], "Very Hard")
]

for tiles, difficulty in initial_states:
    board = Board(tiles)
    print(f"Testing {difficulty} puzzle:")
    solution = a_star_search(board)
    if solution:
        print(f"Solved in {len(solution) - 1} moves.\n")
    else:
        print("No solution found.\n")

'''