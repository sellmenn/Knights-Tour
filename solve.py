import time
import sys
from progress.bar import Bar
from game import *

N = 8 # Default length of board of size N*N
MAX = 5000000 # Cycle limit for search algorithm
START = (0,0) # Initial position of piece
H_PROB = 0.4 # Probability that Warnsdorff’s Rule is conformed to when adding Node objects to Frontier
VAR = "OPEN" # Knights Tour Variation (OPEN or CLOSED)
FILE_NAME = "Solutions/OpenTour.txt" # Save solutions to this default file name

class Frontier:
    def __init__(self):
        self.list = []

    def add(self, node):
        self.list.append(node)

class Stack(Frontier):
    def remove(self):
        return self.list.pop(-1)

# Class to locate branches in Knight object's path
class Node:
    def __init__(self, coordinate, next):
        self.coordinate = coordinate # Coordinate where node was created
        self.next = next # Following coordinate from where node was created


def main():
    try:
        if len(sys.argv) == 4:
            global VAR, N, FILE_NAME
            VAR, N, FILE_NAME = str(sys.argv[1]).upper(), int(sys.argv[2]), sys.argv[3]
            if VAR != "OPEN" and VAR != "CLOSED":
                raise ValueError
    except:
        print("Usage: python3 solve.py open/closed int filename.txt")
        return 1

    # Inititalise Knight and Board objects
    piece = Knight(position=START, board=Board(length=N))
    # Show start board state in terminal
    print(f"\nSearch for {VAR.capitalize()} Knights-Tour solutions in board of size {N}*{N}, H_PROB={H_PROB}, with starting position on {START}:\n")
    piece.board.mark(piece.position, piece.counter)
    print(f"{piece.board}\n")
    # Search for solutions
    solutions = search_path(piece)
    if solutions:
        print(f"\n{solutions} solutions found.\nSolutions saved to {FILE_NAME}.\n")
    else:   
        print(f"\nNo solutions found.\n")
    

def search_path(piece, start=START, h_prob=H_PROB, var=VAR, limit=MAX, file_name=FILE_NAME):
    # Access path of Knight object, and create Frontier object
    path = piece.path
    frontier = Stack()
    # Keep track if number of solutions found
    solution_count = 0
    # Time tracking
    start_time = time.time()
    # Find playable moves at starting position
    current_position = piece.position
    available_moves = piece.sorted_moves(h_prob)
    # Create new node for each playable move
    for move in available_moves:
        new_node = Node(current_position, move)
        # Add new node to frontier
        frontier.add(new_node)
    with Bar("Searching...", max=limit) as bar:
        # While cycle limit is not exceeded
        for i in range(limit):
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
            piece.board.mark(current_position, piece.counter)
            # Add current position to path
            path.append(current_position)
            # Check if board has been fully filled
            if piece.board.check_board():
                if var == "CLOSED" and piece.closed_tour(piece.position, start):
                    solution_count += 1
                    # Write solution into file
                    write_solution(piece.board.map, solution_count, file_name, h_prob, start)
                elif var == "OPEN" and not piece.closed_tour(piece.position, start):
                    solution_count += 1
                    # Write solution into file
                    write_solution(piece.board.map, solution_count, file_name, h_prob, start)
            # For new position, find playable moves
            available_moves = piece.sorted_moves(h_prob)
            # If playable moves exist
            if available_moves:
                # Create new node for each playable move
                for move in available_moves:
                    new_node = Node(current_position, move)
                    # Add new node to frontier
                    frontier.add(new_node)
            # If no playable moves exist, backtrack
            elif not available_moves and frontier.list:
                backtrack(piece, frontier)
            bar.next()
    print(f"\nSearch completed in {time.time() - start_time} seconds.")
    return solution_count


def backtrack(piece, frontier):
        # Access path of Knight object
        path = piece.path
        # If unexplored path exists, stop backtracking
        if piece.position == frontier.list[-1].coordinate:
            return True
        # Unmark current position
        current_position = piece.position
        piece.board.unmark(current_position)
        # Minus from move count
        piece.counter -= 1
        # Remove position from path
        path.pop(-1)
        # If backtracked to start return False
        if len(path) == 0:
            return False
        # Move piece to previous position
        piece.move(path[-1])
        current_position = piece.position
        # If current position has no unexplored paths, recursively backtrack
        if piece.position != frontier.list[-1].coordinate:
            backtrack(piece, frontier)


def write_solution(map, solution_count, file_name, h_prob, start):
    if solution_count == 1:
        with open(file_name, "w") as file:
            file.write(f"Solutions for {N}*{N} {VAR.capitalize()} Knights-Tour Problem, H_PROB={h_prob}, with piece initially at {start}:\n\n")
    with open(file_name, "a") as file: 
        file.write(f"Solution {solution_count}:\n")
        for row in map:
            file.write(f"{row}\n")
        file.write("\n")


if __name__ == "__main__":
    main()