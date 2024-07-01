# THE KNIGHT'S TOUR PROBLEM
"A knight's tour is a sequence of moves of a knight on a chessboard such that the knight visits every square exactly once. If the knight ends on a square that is one knight's move from the beginning square (so that it could tour the board again immediately, following the same path), the tour is closed (or re-entrant); otherwise, it is open." - Wikepedia
---


# PROJECT DESCRIPTION
This project aims to find solutions to both open and closed variants of the Knight's Tour problem, given a board with sides of length N squares.

### Inititally, the project's scope only included the open variant of the problem.
The code was designed around a naive backtracking approach, incorporating the use of a frontier with a stack (LIFO) configuration, to obtain a single solution. However, upon testing, it was found that past N = 7, the code would take too long to run, with iterations in excess of 10000000 required before a single solution could be found. To overcome this obstacle, a version of Warnsdorff’s Rule was used to approach the problem, in addition to backtracking: Always move the knight to an adjacent, unvisited square with minimal degree. Starting from any square, the knight must move to an unvisited square that has the fewest successive moves. With this technique, it was found that only a fraction of the original iterations was required to generate a single solution. This opened up the possibility of searching for multiple solutions to the open problem, hence the project was modified to generate multiple solutions instead.

### The project's scope was later expanded to include the closed variant of the problem.
At this point, the program was able to reliably find solutions to the open variant. In a span of 2 minutes, the program was able to find 30000 unique solutions to the variant. During experimentation to search for solutions for the closed variant, it was found that the program would crash prematurely before any solution could be found. To circumvent this, the code was modified to write solutions directly to a text file, instead of storing solutions in memory. It was also found that when the program did not entirely conform to Warnsdorff’s Rule, solutions were found more quickly for this variant of the problem. Hence, a new global variable 'H_PROB' was added to the program to allow for configuration of how much the rule is adhered to.


# HOW TO RUN
1. Ensure all modules in requirements.txt have been installed. Simply use 'pip3 install -r requirements.txt' in your terminal.
2. Type 'python3 solve.py' in your terminal. Hit enter. 
3. By default, the program will search for solutions to the open variant of the problem.
4. By default, the program will write solutions to 'solutions/OpenTour.txt'. The program also defaults to a board size of 8, with H_PROB=1
5. Refer to the following section about configuration of global variables.
6. Alternatively, use the following command line argument: python3 solve.py open/closed int filename.txt

## Configuring Global Variables
- To search for solutions to the open variant (VAR="OPEN"), it is recommended that H_PROB be set to 1 for maximum efficiency.
- To search for solutions to the closed variant(VAR="CLOSED"), it is recommended that H_PROB be varied between 0 and 1, depending on board size.

### Test Configurations and Results
**Open Variant:**
- 8*8 board, MAX=5000000, START=(0,0), H_PROB=1, 17521 solutions found.
- 8*8 board, MAX=5000000, START=(0,0), H_PROB=0.4, 0 solutions found.

**Closed Variant:**
- 6*6 board, MAX=10000000, START=(0,0), H_PROB=0.5, 114 Solutions found.
- 6*6 board, MAX=5000000, START=(0,0), H_PROB=0.4, 234 Solutions found.

It is interesting to note that the heuristic function has greater utility in searchig for solutions to the open variant, in contrast with that of the closed variant.

# PROJECT CONTENT

The project includes two files: 
1. game.py - contains the **Board** and **Knight** class.
2. solve.py - contains code to solve the problem.

## Board and Knight Class
The Board class includes instance methods to simulate a chess board.
The Knight class includes instance methods to simulate a knight chess piece. The Knight class also contains a 'path' attribute which keeps tracks of coordinates a Knight object has visited.

Notably, the Knight class contains the following instance methods cruicial to tackling the problem.
* self.available_moves() returns a list of legal moves - moves within the confines of the board. It takes in an optional bool argument 'visited' to configure if previously visited coordinates should be excluded or not.
* self.informed_move() returns a legal move with the fewest successive moves
* self.sorted_moves() returns a list of legal moves, sorted according to Warnsdorff’s Rule. It takes in an optional argument 'prob' which determines whether or not the rule is conformed to.

## solve.py

### Stack Class
This class inherits from the frontier class. The **Stack** class was created according to the last-in-first-out principle. This principle was chosen as the approach being used is similar to a depth-first-search: in that we are following the best possible path according to Warnsdorff’s Rule, until a dead-end is reached (no more legal moves available).
self.remove() handles the removing of a node object from the last position in the frontier while returning the removed node object.

### Node Class
This class is relied on to determine 'branches' in the path of the knight piece. 'coordinate' contains the x,y coordinate of a square the knight piece has visited, and 'next' contains the x,y coordinate of the knight piece's subsequent move.

### search_path(piece)
The backbone to solving the problem, this function takes in two arguments 'piece', a Knight object, and a Frontier object.
1. For every move made, nodes are added to the frontier.
2. A node is then removed from the frontier, containing the next possible best move.
3. Knight object is moved to the new coordinate, according to the node.
4. If the board has been fully traversed, check if it has completed a closed or open loop. Write any solution into file.
5. If the frontier is empty, then there are no more moves to be played, and the function terminates.
6. If no available moves can be generated at a square, the **backtrack** function is called.

### backtrack(piece)
In this project's implementation of backtracking, we rely on 'coordinate' in the Node class to identify branches in the knight piece's path, and remove moves from 'path' in the Knight class until the previous branch is located (last coordinate in 'path' matches 'coordinate' for last node in frontier). Essentially, when backtrack is called:
1. Move knight piece 1 step back
2. If current coordinate does not match most recent node's 'coordinate' in frontier, no other moves can be made from current coordinate. Go back to step 1.
Hence, we recursively call backtrack until a differnt path is found.
