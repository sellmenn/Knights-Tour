import time
from progress.bar import Bar
from game import *

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


"""
Function which takes in the folllowing arguments:
length - length of Board object (defaults to 8)
start - starting coordinate of Knight object (defaults to (0, 0))
h_prob - probability that Warnsdorff's Rule is conformed to in path finding (defaults to 1)
var - 'open' or closed' Knight's Tour variant (defaults to 'OPEN')
limit - maximum number of iterations (defaults to 500000)
file_name - name of '.txt' file to write solutions to (defaults to "Open_KT.txt")

Writes solutions for tours found directly to file_name provided.
Returns the number of tours found for the given configuration, within the limit allowed.
"""
def find_KT(length=8, start=(0,0), h_prob=1, var="OPEN", limit=500000, file_name="Open_KT.txt"):
    # Create Knight object
    piece = Knight(position=start, board=Board(length=length))
    # Access path of Knight object, and create Frontier object
    path = piece.path
    frontier = Stack()
    # Keep track if number of solutions found
    solution_count = 0
    # Time tracking
    start_time = time.time()
    current_position = piece.position
    # Mark starting position
    piece.board.mark(current_position, piece.counter)
    # Find playable moves at starting position
    available_moves = piece.sorted_moves(h_prob)
    # Create new node for each playable move
    for move in available_moves:
        # Add new node to frontier
        frontier.add(Node(current_position, move))
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
            if piece.board.complete():
                if var == "CLOSED" and piece.closed_tour(piece.position, start):
                    solution_count += 1
                    # Write solution into file
                    write_solution(piece, solution_count, file_name, h_prob, start, var, limit)
                elif var == "OPEN" and not piece.closed_tour(piece.position, start):
                    solution_count += 1
                    # Write solution into file
                    write_solution(piece, solution_count, file_name, h_prob, start, var, limit)
            # For new position, find playable moves
            available_moves = piece.sorted_moves(h_prob)
            # If playable moves exist
            if available_moves:
                # Create new node for each playable move
                for move in available_moves:
                    # Add new node to frontier
                    frontier.add(Node(current_position, move))
            # If no playable moves exist, backtrack
            elif not available_moves and frontier.list:
                backtrack(piece, frontier)
            bar.next()
    print(f"Search completed in {(time.time() - start_time):.4f} seconds.")
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


def write_solution(piece, solution_count, file_name, h_prob, start, var, limit):
    map = piece.board.map
    if solution_count == 1:
        with open(file_name, "w") as file:
            file.write(f"{var.capitalize()} Knight's Tour Problem\nLength of board: {piece.board.length}\nH_PROB: {h_prob}\nStarting coordinate: {start}\nSearch depth: {limit}\n\n")
    with open(file_name, "a") as file: 
        file.write(f"Solution {solution_count}:\n")
        for row in map:
            file.write(f"{row}\n")
        file.write("\n")