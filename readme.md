## The Knight's Tour

"A knight's tour is a sequence of moves of a knight on a chessboard such that the knight visits every square exactly once. If the knight ends on a square that is one knight's move from the beginning square (so that it could tour the board again immediately, following the same path), the tour is closed (or re-entrant); otherwise, it is open." - Wikipedia

This project aims to find solutions to both open and closed Knight's Tours variants.

## Timeline

##### Initial objective: Find a single solution to the open variant of the problem, given a starting coordinate.

The code was designed around a naive backtracking approach, incorporating the use of a frontier with a stack configuration, to obtain a single solution, given a starting coordinate. 
Upon testing, it was found that past a board size of 7, the code would take too long to run, with iterations in excess of 10000000 required before a single solution could be found. 
To overcome this, a version of Warnsdorff’s Rule was used in addition to backtracking: From any square, the knight must move to an unvisited square that has the fewest successive moves. With this technique, it was found that only a fraction of the original iterations was required to generate a single solution. 


##### 1st Revision: Find multiple solutions to the open variant of the problem, given a starting coordinate.

The improvements in search times opened up the possibility of searching for multiple solutions to the open problem, hence the project was modified to generate multiple solutions instead. In a span of 2 minutes, the program was able to find 30000 unique solutions to the variant.


##### 2nd Revision: Find multiple solutions to either open or closed variants of the problem, given a starting coordinate.

The scope was expanded to include the closed variant of the problem.  During experimentation, it was found that the program would crash prematurely before any solution could be found. To avoid this, the code was modified to write solutions directly to a text file, instead of storing solutions in memory.


##### 3rd Revision: Find multiple solutions to either open or closed variants of the problem, starting from every coordinate of the board.

It was observed that the number of closed tours that could be found varied between starting coordinates. Hence, the project was redesigned to search for either open or closed tours starting from anywhere on the board. 
To allow for easy comparison, the starting coordinate and associated tours are sorted into individual '.txt' files as well as summarised in a '.csv' file.

## Obtained Results

For board of length 8 and search depth of 800000:

| Variant | Tours found | Time / sec |
| ------- | ----------- | ---------- |
| Open    | 351 986     |   509.80   |
| Closed  | 60 164      |   532.16   |

## Usage
1. Use `pip3 install -r requirements.txt` in your terminal to ensure all required modules have been installed.
2. Command line argument usage: `python3 analyse.py open/closed length` or `python3 analyse.py`.

> Accessing Results:
>> The program will create an empty directory 'Results' if it does not already exist, where solutions are sorted into individual '.txt' files.
>>> e.g. 'Open_12.txt' for solutions to the open variant stemming from coordinate (1,2).
>> Data is summarised in a separate csv file 'Open_KT.csv' or 'Closed_KT.csv'.

> Further Configuration:
>> 
- The global variable `MAX` in analyse.py can be varied to adjust the depth of search for each starting coordinate. The default setting of 500000 results in an approximate run-time of 330 seconds.
- The global variable `H_PROB` in analyse.py can be varied between 0 and 1 to adjust the conformity to Warnsdorff’s Rule.

## PROJECT IMPLEMENTATION
The project includes three files: 
1. util.py - contains the `Board and Knight class.
2. search.py - contains the Stack and Node class, find_KT() and backtrack() functions.
3. analyse.py - contains the  analyse_KT() function.

## util.py

#### Board Class
This class includes instance methods to simulate a chess board. The Board class contains a 'map' attribute which stores the layout of the board as a list, as well as a 'length' attribute.
* self.create() takes in an optional 'map' argument of type list, and assigns it to the 'map' attribute. If none is provided, it defaults to creating a 'map' according to its 'length' attribute.
* self.mark() takes in a 'coordinate' and 'marker' as arguments. It assigns the marker to the coordinate specified in the 'map' attribute.
* self.unmark() takes in a 'coordinate' as an argument, and resets the coordinate specified in the 'map' attribute to 0.
* self.complete() returns True if all coordinates in the 'map' attribute have been marked, and False otherwise.
* self.check_square() returns True if the specified coordinate in the 'map' attribute has been marked, and False otherwise.

#### Knight Class
This class includes instance methods to simulate a knight chess piece. The Knight class contains a 'path' attribute which keeps tracks of coordinates a Knight object has visited, a Board object, a 'counter' attribute which tracks the number of squares it has already traversed on a Board, and a 'position' attribute which represents the Knight object's current coordinate on the Board object.
Notably, it contains the following instance methods crucial to tackling the problem.
* self.available_moves() returns a list of legal moves within the confines of the board. It takes in an optional bool argument 'visited' to configure if previously visited coordinates should be excluded or not.
* self.informed_move() returns a legal move with the fewest available successive moves.
* self.sorted_moves() returns a list of legal moves, sorted according to Warnsdorff’s Rule. It takes in an optional argument 'prob' which determines whether or not the rule is conformed to.
* self.closed_tour() takes in 2 coordinates as arguments, and returns True if they are one move apart from each other.

## search.py

#### Stack Class
The Stack class was created according to the last-in-first-out principle. This principle was chosen as the approach being used is similar to a depth-first-search: in that we are following the best possible path according to Warnsdorff’s Rule, until a dead-end is reached (no more legal moves available).
self.remove() handles the removing of a node object from the last position in the frontier while returning the removed node object.

#### Node Class
This class is relied on to determine 'branches' in the path of the knight piece. 'coordinate' contains the x,y coordinate of a square the knight piece has visited, and 'next' contains the x,y coordinate of the knight piece's subsequent move.

#### find_KT()
This function takes in the following 6 arguments:
- length - length of Board object (defaults to 8)
- start - start coordinate of Knight object (defaults to (0, 0))
- h_prob - probability that Warnsdorff's Rule is conformed to in path finding (defaults to 1)
- var - 'open' or closed' Knight's Tour variant (defaults to 'OPEN')
- limit - maximum number of iterations (defaults to 500000)
- file_name - name of '.txt' file to write solutions to (defaults to "Open_KT.txt")

Solutions to knight's tours are written directly to 'file_name'.
The function returns the number of tours found for the given configuration, within the limit allowed.
1. At any position, Node objects are added to the Stack to keep track of branches in the Knight's path.
2. A Node is then removed from the Stack, containing the next move to be made.
3. The Knight is moved to the corresponding coordinate.
4. If the board has been fully traversed, check if it has completed a closed or open loop. Write solution into file.
5. If the frontier is empty, then there are no more moves to be played, and the function terminates.
6. If no more moves can be played from the current position, the **backtrack** function is called.

#### backtrack()
In this project's implementation of backtracking, we rely on 'coordinate' in the Node class to identify branches in the Knight's path, and remove moves from 'path' in the Knight class until the previous branch is located (last coordinate in 'path' matches 'coordinate' for last node in frontier). Essentially, when backtrack is called:
1. Move knight piece 1 step back
2. If current coordinate does not match most recent node's 'coordinate' in frontier, no other moves can be made from current coordinate. Go back to step 1.
Hence, we recursively call backtrack until a differnt path is found.

## analyse.py

#### analyse_KT()
This function serves as the core routine, streamlining the search process and organising results in designated output files. 
It works by calling find_KT for each coordinate on a Board object, and writing its solutions into separate `.txt` files for each coordinate.
It also writes the number of solutions found from every coordinate into a `.csv` file.
Progress can be monitored through terminal outputs for each starting coordinate. 