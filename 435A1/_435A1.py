import time
import sys
import queue

class TreeSearchNode:

    parent = None
    path = []

    def __init__(self, newParent: TreeSearchNode = None, newPath: list = []):
        parent = newParent
        path = newPath

    def editParent(newParent: TreeSearchNode):
        parent = newParent

    def getParent():
        return parent




goalState = "123456789ABCDEF "
def main():
    stats = [0, 0, 0, 1] #statistics to be printed at the end. Idx 0 is depth,
    #idx 1 is number created, idx 2 is num expanded, idx 3 is fringe size
    puzzle = sys.argv[1]
    method = sys.argv[2]
    if method == "BFS":
        bfs(puzzle)
    exit()

def bfs(puzzle: str, stats):
    copy = puzzle
    solved = puzzle == goalState
    visited = {}
    q = queue.Queue(-1)

    if isSolveable(puzzle) == False:
        stats[0] = -1
        stats[3] = 0
    while not(solved):
        true 


def moveSpace(puzzle: str, idx, dir) -> {bool, str}:
    result = [False, ""]
    if dir == "Up":
        if not(0<=idx<=3) :
            result = [True, swapChars(puzzle, idx, idx-4)]
    elif dir == "Down":
         if not(12<=idx<=15) :
            result = [True, swapChars(puzzle, idx, idx+4)]
    elif dir == "Left":
         if not(idx in (0,4,8,12)) :
            result = [True, swapChars(puzzle, idx, idx-1)]
    elif dir == "Right":
        if not(idx in (3,7,11,15)) :
            result = [True, swapChars(puzzle, idx, idx+1)]
    return result

def swapChars(string: str, idx1, idx2) -> str:
    moved = string
    moved = list(moved) #convert the string to list so elements can be swapped
    temp = moved[idx2]
    moved[idx2] = moved[idx1]
    moved[idx1] = temp
    moved = str(moved) #convert list back into a string
    return moved

def isSolvable(puzzle: str) -> bool:#check if the given puzzle is solveable
    intcpy = [0] * 16
    emptyidx = -1
    for i in range(0, len(puzzle)) :
        c = puzzle[i]
        charval = ord(c)
        if 48<=charval<=57 :
            intcpy[i] = charval - 48
        elif 65<=charval<=70:
            intcpy[i] = charval - 55
        elif charval == 32:
            intcpy[i] = 0
            emptyidx = i

    inversioncnt = 0
    for a in range(0, len(intcpy)):
        inversioncnt += intcpy[a] - 1
        if a>0 and intcpy[a] != 1:
            for num in intcpy[0:a-1]:
                if num<intcpy[a]:
                    inversioncnt -= 1
    solveable = False;
    if (0<=emptyidx<=3 or 8<=emptyidx<=11) and inversioncnt % 2 == 1:
        solveable = True
    elif (4<=emptyidx<=7 or 12<=emptyidx<=15) and inversioncnt % 2 == 0:
        solveable = True
    return solveable


        
            
'''if __name__ == "__main__":
    main()'''




