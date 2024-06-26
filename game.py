from copy import deepcopy
from random import shuffle, choices

class Board:
    def __init__(self, length = 6, map = list()):
        self.length = length
        self.map = self.create(map)

    # Instance method to return board as a str object
    def __repr__(self):
        map_str = str()
        for row in self.map:
            map_str += f"{row}\n"
        return map_str

    # Function to return board as list
    def create(self, map = list()):
        board = list()
        if not map:
            for i in range(self.length):
                board.append(list())
                for j in range(self.length):
                    board[i].append(0)
            return board
        return map

    # Function to mark coordinate on board with a marker
    def mark(self, coordinate, marker):
        x, y = coordinate
        self.map[x][y] = marker

    # Function to unmark position on board
    def unmark(self, coordinate):
        x, y = coordinate
        self.map[x][y] = 0

    # Function to check if all of board has been marked
    def complete(self):
        for row in self.map:
            for square in row:
                if not square:
                    return False
        return True

    # Function to check if a coordinate on board has been marked
    def check_square(self, coordinate):
        x, y = coordinate
        if self.map[x][y] == 0:
            return False
        return True


class Knight():
    def __init__(self, position = (0,0), board = Board()):
        self.position = position
        self.board = board
        self.counter = 1 # keep track of number of moves played
        self.path = list()

    # Function to return valid moves
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
        valid_moves = []
        for move in moves:
            if 0 <= move[0] < self.board.length and 0 <= move[1] < self.board.length:
                if visited == False:
                    if not self.board.check_square(move):
                        valid_moves.append(move)
                else:
                    valid_moves.append(move)
        return valid_moves
    
    # Function which if given a list of moves, returns a valid move which leads to the position with least available moves
    # Defaults to object's available moves if no list provided
    def informed_move(self, moves = list()):
        min_move = 8
        if not moves and self.available_moves():
                moves = self.available_moves()
        for move in moves:
            if len(self.available_moves(position=move)) <= min_move:
                min_move = len(self.available_moves(position=move))
                best = move
        return best
    
    # Function to return sorted list of valid moves in decreasing order of next available moves
    def sorted_moves(self, prob = 0):
        valid_moves = deepcopy(self.available_moves())
        sorted_moves = []
        while valid_moves:
            best_move = self.informed_move(valid_moves)
            sorted_moves.append(best_move)
            valid_moves.remove(best_move)
        sorted_moves.reverse()
        shuffle_moves = choices([True, False], [1 - prob, prob])[0]
        if shuffle_moves:
            shuffle(sorted_moves)
        return sorted_moves
    
    # Function to move knight to new position
    def move(self, new_position):
        self.position = new_position

    # Function to check if current position on the board is one move away from another position
    def closed_tour(self, coordinate_1, coordinate_2):
        if coordinate_2 in self.available_moves(position=coordinate_1, visited=True):
            return True
        return False

