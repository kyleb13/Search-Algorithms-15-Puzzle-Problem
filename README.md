# TCSS435
This project implements mulltiple different search algorithms for a puzzle known as the 15-puzzle problem. The puzzle is a 4x4 grid of
numbers from 1-9 and letters A-F (and one empty cell). The goal is to get the puzzle from a scrambled state to an ordered state only by
swapping the position of the empty cell and it's adjacent cells. For example:
                  1   2   5   4                         1   2   3   4
                  3   7   8   9                         5   6   7   8
                  6   A       F      needs to become    9   A   B   C
                  C   B   D   E                         D   E   F
                  
To run the program, run _435A1.py from the command line with two arguments: the puzzle, and the search algorithm to use. Format the puzzle
as one string with all of the cells in order (the example i gave earlier would be "125437896A FCBDE"). The second argument, which determines
what algorithm is used, must be one of these options: BFS, DFS, DLS, GBFS, AStar. If you choose GBFS or AStar, you need to give a third
argument that determines which heuristic the algorithm uses (pass either "h1" or "h2")
