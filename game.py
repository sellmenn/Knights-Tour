from random import shuffle
import copy

class Board:
    def __init__(self, length = 6, map = list()):
        self.length = length
        self.set_board(map)

    
    # Function to set board
    def set_board(self, map = list()):
        board = list()
        if len(map) == 0:
            for i in range(self.length):
                board.append(list())
                for j in range(self.length):
                    board[i].append(0)
            self.map = board
        else:
            self.map = map
    
    # Function to print board in terminal
    def print_board(self):
        for row in self.map:
            print(row)

    # Function to mark position on board with n
    def mark_board(self, position, n):
        x, y = position
        self.map[x][y] = n


    # Function to unmark position on board
    def unmark_board(self, position):
        x, y = position
        self.map[x][y] = 0


    # Function to check if all of board has been marked
    def check_board(self):
        for row in self.map:
            for square in row:
                if square == 0:
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

    # Function to return valid moves (that have not been played yet 
    def available_moves(self, position = None):
        if position == None:
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
                if not self.board.check_square(move):
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
    def sorted_moves(self):
        valid_moves = copy.deepcopy(self.available_moves())
        sorted_moves = []
        while valid_moves:
            best_move = self.informed_move(valid_moves)
            sorted_moves.append(best_move)
            valid_moves.remove(best_move)
        sorted_moves.reverse()
        return sorted_moves
    
    
    # Function to move knight to new position
    def move(self, new_position):
        self.position = new_position


