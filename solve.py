import time
import sys
from copy import deepcopy
from progress.bar import Bar
from game import *

N = 8 # Default length of board of size N*N
MAX = 500000 # Cycle limit for search algorithm
START = (0,0) # Initial position of piece
FILE_NAME = "solutions.txt" # Save solutions to this default file name

class Frontier:
    def __init__(self):
        self.list = []

    def add(self, node):
        self.list.append(node)

class Stack(Frontier):
    def remove(self):
        return_value = self.list.pop(-1)
        return return_value

# Class to pass data between functions
class Solution:
    def __init__(self, path = list(), frontier = Stack()):
        self.path = path # Stores path of Knight object
        self.frontier = frontier # Stores nodes
        self.data = list() # Store deep copies of solutions
        self.n = 0 # N value - length of Board object
        self.time = 0.0 # Time taken to obtain solutions
        self.length = 0 # Number of solutions

# Class to locate branches in Knight object's path
class Node:
    def __init__(self, coordinate, next):
        self.coordinate = coordinate # Coordinate
        self.next = next


def main():
    try:
        if len(sys.argv) == 3:
            n = int(sys.argv[1])
            file_name = sys.argv[2]
        else:
            file_name, n = FILE_NAME, N
    except:
        print("Usage: python3 solve.py int filename.txt")
        return 1

    # Create knight and board objects
    piece = Knight(position=START, board=Board(length=n))

    # Show start state in terminal
    print(f"\nSearch for solutions in board of size {n}*{n}, with starting position on {START}:\n")
    piece.board.mark_board(piece.position, piece.counter)
    piece.board.print_board()
    print()

    # Solve function
    solution = search_path(piece)
    solutions = solution.data
    solution.n = n

    # If solutions exist, print solutions
    if solutions:
        write_solution(solution, file_name)
        print(f"\nSearch completed in {solution.time} seconds.\n{solution.length} solutions found.\nSolutions saved to {file_name}.\n")
    else:   
        print(f"\nNo solutions found.\n")


def write_solution(solution, file_name):
    solutions = solution.data
    n = solution.n
    count = 0
    with open(file_name, "w") as file:
            file.write(f"Solutions for {n}*{n} Knight's Tour Problem, with piece initially at {START}:\n\n")
            for board in solutions:
                count += 1
                file.write(f"Solution {count}:\n")
                for row in board.map:
                    file.write(f"{row}\n")
                file.write("\n")
            file.write(f"\nSearch completed in {solution.time} seconds.\n{solution.length} solutions found.")
    

def search_path(piece):
    # Create empty path and frontier
    solution = Solution()
    frontier, path = solution.frontier, solution.path

    # keep track of solutions
    solutions = solution.data

    # Time tracking
    start_time = time.time()

    # For starting position, find playable moves
    current_position = piece.position
    available_moves = piece.available_moves()

    # Create new node for each playable move
    for move in available_moves:
        new_node = Node(current_position, move)
        # Add new node to frontier
        frontier.add(new_node)

    with Bar("Searching...", max=MAX) as bar:
        # While cycle limit is not exceeded
        for i in range(MAX):

            # If frontier is empty, no solutions exist
            if not frontier.list:
                break
            
            # Pick a node from frontier
            node = frontier.remove()

            # Move piece to new position
            piece.move(node.next)
            # Add to move count
            piece.counter += 1

            # Update current position
            current_position = piece.position

            # Mark position as played
            piece.board.mark_board(current_position, piece.counter)
            # Add current position to path
            path.append(current_position)

            # Check if board has been fully filled
            if piece.board.check_board():
                solution_map = deepcopy(piece.board.map)
                # Keep a copy of solution
                solutions.append(Board(length=N, map=solution_map))
                solution.length += 1

            # For new position, find playable moves
            available_moves = piece.sorted_moves()

            # If playable moves exist
            if available_moves:
                # Create new node for each playable move
                for move in available_moves:
                    new_node = Node(current_position, move)
                    # Add new node to frontier
                    frontier.add(new_node)
    

            # If no playable moves exist, backtrack
            elif not available_moves and frontier.list:
                backtrack(piece, solution)

            bar.next()

    solution.time = time.time() - start_time

    return solution


def backtrack(piece, solution):
        # Access frontier and path
        frontier = solution.frontier
        path = solution.path

        # If unexplored path exists, stop backtracking
        if piece.position == frontier.list[-1].coordinate:
            return True

        # Unmark current position
        current_position = piece.position
        piece.board.unmark_board(current_position)

        # Minus from move count
        piece.counter -= 1

        # Remove position from path
        path.pop(-1)

        # If backtracked to start or frontier is empty, return False
        if len(path) == 0:
            return False
        
        # Move piece to previous position
        piece.move(path[-1])
        current_position = piece.position

        # If current position has no unexplored paths, recursively backtrack
        if piece.position != frontier.list[-1].coordinate:
            backtrack(piece, solution)


if __name__ == "__main__":
    main()
