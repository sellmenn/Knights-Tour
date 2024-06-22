# THE OPEN KNIGHT'S TOUR PROBLEM
"A knight's tour is a sequence of moves of a knight on a chessboard such that the knight visits every square exactly once. If the knight ends on a square that is one knight's move from the beginning square (so that it could tour the board again immediately, following the same path), the tour is closed (or re-entrant); otherwise, it is open." - Wikepedia

--- 

# HOW TO RUN
1. Ensure all modules in requirements.txt have been installed. Simply use 'pip3 install -r requirements.txt' in your terminal.
2. Type 'python3 solve.py' in your terminal. Hit enter. 
3. By default, the program will write solutions to 'solutions.txt'. The program also defaults to a board size of 8.
4. To configure board size (int) and output file name, type 'python3 solve.py int filename.txt' instead. Alternatively, modify the global variables in solve.py.

# PROJECT DESCRIPTION
This project aims to find solutions to the open variant of the Knight's Tour problem, given a board with sides of N squares.

The code was initially designed around a backtracking approach, incorporating the use of a frontier with a stack (LIFO) configuration, to obtain a single solution. However, upon testing, it was found that past N = 7, the code would take too long to run, with iterations in excess of 10000000 required before a solution could be found.

To overcome this obstacle, a version of Warnsdorff’s Rule was used to approach the problem, in addition to backtracking. Always move the knight to an adjacent, unvisited square with minimal degree. Starting from any square, the knight must move to an unvisited square that has the fewest successive moves.

With this technique, it was found that only a fraction of the original iterations was required to generate a single solution. This opened up the possibility of searching for multiple solutions to the problem, hence the project was modified to generate multiple solutions instead.

The project includes two files: 
1. game.py - contains the **Board** and **Knight** class.
2. solve.py - code to solve the problem.

## Board and Knight Class
The Board class includes instance methods to simulate a chess board.
The Knight class includes instance methods to simulate a knight chess piece.

Notably, the Knight class contains the following instance methods crucial to tackling the problem.
* self.available_moves() returns a list of legal moves - moves within the confines of the board which have not been visitied
* self.informed_move() returns a legal move with the fewest successive moves
* self.sorted_moves() returns a list of legal moves, sorted according to Warnsdorff’s Rule.

## Solve.py

### Solution Class
To aid in the ease of passing multiple data types between functions, the **Solution** class contains information about the solutions to the problem. For example: path taken to final solution, frontier, number of unique obtained solutions, time taken to obtain solutions.

### Stack Class
This class inherits from the frontier class. The **Stack** class was created according to the last-in-first-out principle. This principle was chosen as the approach being used is similar to a depth-first-search: in that we are following the best possible path according to Warnsdorff’s Rule, until a dead-end is reached (no more legal moves available).
self.remove() handles the removing of a node object from the last position in the frontier while returning the removed node object.

### Node Class
This class is relied on to determine 'branches' in the path of the knight piece. 'coordinate' contains the x,y coordinate of a square the knight piece has visited, and 'next' contains the x,y coordinate of the knight piece's subsequent move.

### search_path(piece)
The backbone to solving the problem, this function takes in a single argument 'piece' which represents a Knight object.
1. For every move made, nodes are added to the frontier.
2. A node is removed from the frontier, containing the next possible best move.
3. Knight object is moved to the new coordinate, according to the node.
4. If the frontier is empty, then there are no more moves to be played, and the function terminates.
5. If no available moves can be generates at a square, the **backtrack** function is called.

### backtrack(piece)
In this project's implementation of backtracking, we rely on 'coordinate' in the Solution class to identify branches in the knight piece's path, and remove moves from 'path' in the solution class until the previous branch is located (last coordinate in 'path' matches 'coordinate' for last node in frontier). Essentially, when backtrack is called:
1. Move knight piece 1 step back
2. If current coordinate does not match most recent node's 'coordinate' in frontier, no other moves can be made from current coordinate. Go back to step 1.
Hence, we recursively call backtrack until a differnt path is found.
