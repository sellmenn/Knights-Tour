from copy import deepcopy
from random import shuffle, choices

class Board:
    def __init__(self, length = 6, map = list()):
        self.length = length
        self.map = self.create(map)
        self.visited = dict()
        self.visited_count = 0

    # Method to return board as a str object
    def __repr__(self):
        map_str = str()
        for row in self.map:
            map_str += f"{row}\n"
        return map_str

    # Method to return board as list
    def create(self, map = list()):
        board = list()
        if not map:
            for i in range(self.length):
                board.append(list())
                for j in range(self.length):
                    board[i].append(0)
            return board
        return map

    # Method to mark coordinate on board with a marker
    def mark(self, coordinate, marker):
        self.visited[coordinate] = True
        self.visited_count += 1
        x, y = coordinate
        self.map[x][y] = marker

    # Method to unmark position on board
    def unmark(self, coordinate):
        self.visited[coordinate] = False
        self.visited_count -= 1
        x, y = coordinate
        self.map[x][y] = 0

    # Method to check if all of board has been marked
    def complete(self):
        if self.visited_count < self.length ** 2:
            return False
        return True

    # Method to check if a coordinate on board has been marked
    def check_square(self, coordinate):
        if coordinate not in self.visited:
            return False
        elif not self.visited[coordinate]:
            return False
        return True


class Knight():
    def __init__(self, position = (0,0), board = Board()):
        self.position = position
        self.board = board
        self.counter = 1 # keeps track of number of moves played
        self.path = list()

    # Method to return valid moves
    def available_moves(self, position = None, visited = False):
        if not position:
            x, y = self.position
        else:
            x, y = position
        moves = [
            (x + 2, y + 1),
            (x + 1, y + 2),
            (x - 1, y + 2),
            (x - 2, y + 1),
            (x - 2, y - 1),
            (x - 1, y - 2),
            (x + 1, y - 2),
            (x + 2, y - 1)]
        valid_moves = list()
        for move in moves:
            if 0 <= move[0] < self.board.length and 0 <= move[1] < self.board.length:
                if visited == False:
                    if not self.board.check_square(move):
                        valid_moves.append(move)
                else:
                    valid_moves.append(move)
        return valid_moves
    
    # Method which if given a list of moves, returns a valid move which leads to the position with least available moves
    """
    Previous Implementation
    def informed_move(self, moves = list()):
        min_move = 8
        if not moves: 
                moves = self.available_moves()
        for move in moves:
            degree_of_move = len(self.available_moves(position=move)) # number of subsequent available moves
            if degree_of_move <= min_move:
                min_move = degree_of_move
                best = move
        return best
    """
    
    # Method which if given a list of moves, returns a list of tuples containing degree-move pairs
    def informed_moves(self, moves = list()):
        informed_moves = list()
        if not moves: moves = self.available_moves()
        for move in moves:
            degree_of_move = len(self.available_moves(position=move)) # number of subsequent available moves
            informed_moves.append((degree_of_move, move))
        informed_moves.sort(reverse=True)
        return informed_moves

    
    # Method to return sorted list of valid moves in decreasing order of next available moves
    def sorted_moves(self, prob = 0):
        shuffle_moves = choices([True, False], [1 - prob, prob])[0]
        valid_moves = self.available_moves()
        if shuffle_moves:
            shuffle(valid_moves)
            return valid_moves
        sorted_moves = list()
        """
        Previous implementation:
        while valid_moves:
            best_move = self.informed_move(valid_moves)
            sorted_moves.append(best_move)
            valid_moves.remove(best_move)
        sorted_moves.reverse()
        """
        informed_moves = self.informed_moves(valid_moves)
        for move in informed_moves:
            sorted_moves.append(move[1])
        return sorted_moves
    
    # Method to move knight to new position
    def move(self, new_position):
        self.position = new_position

    # Method to check if current position on the board is one move away from another position
    def closed_tour(self, coordinate_1, coordinate_2):
        if coordinate_2 in self.available_moves(position=coordinate_1, visited=True):
            return True
        return False