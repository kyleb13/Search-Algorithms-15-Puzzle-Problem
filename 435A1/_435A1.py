import time
import sys
import queue

class TreeSearchNode:

    def __init__(self, newParent, newPath: list = [], newState: str = " ", newDepth: int = 0):
        self.__parent = newParent
        self.__path = newPath
        self.__state = newState
        self.__spaceLocation = self.__state.find(" ")
        self.__depth = newDepth

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.getState() == other.getState()

    def getParent(self):
        return self.__parent

    def getPath(self) ->[]:
        retpath = self.__path.copy()
        return retpath
    
    def getState(self) -> str:
        copystate = self.__state
        return copystate

    def getSpaceLocation(self) -> int:
        return self.__spaceLocation

    def getDepth(self) -> int:
        return self.__depth



goalState1 = "123456789ABCDEF "
goalState2 = "123456789ABCDFE "
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
    visited = {}
    q = queue.Queue(-1)
    q.put(TreeSearchNode(None, [copy], copy, 0))
    expandNode = q.get()
    children = []
    temppath = []
    while expandNode.getState() != goalState1 and expandNode.getState() != goalState2:
        visited[expandNode.getState()] = [expandNode]
        children.append(moveSpace(expandNode.getState(), expandNode.getSpaceLocation(), "Right"))
        children.append(moveSpace(expandNode.getState(), expandNode.getSpaceLocation(), "Down"))
        children.append(moveSpace(expandNode.getState(), expandNode.getSpaceLocation(), "Left"))
        children.append(moveSpace(expandNode.getState(), expandNode.getSpaceLocation(), "Up"))
        for el in children:
            if el[0] == True:
                temppath = expandNode.getPath()
                temppath.append(el[1])
                if el[1] not in visited:
                    q.put(TreeSearchNode(expandNode, temppath, el[1], expandNode.getDepth() + 1))
                    stats[1] += 1
        stats[2] += 1
        if q._qsize() > stats[3]:
            stats[3] = q._qsize()
        expandNode = q.get()
        children.clear()
    stats[0] = expandNode.getDepth()
    print("Goal State Found!")
    print("Path to goal state:")
    printSolution(expandNode.getPath(), stats)


def dls(puzzle: str, stats, maxdepth: int, limited: bool) -> bool:
    copy = puzzle
    visited = {}
    stack = []
    stack.append(TreeSearchNode(None, [copy], copy, 0))
    expandNode = stack.pop()
    children = []
    temppath = []
    searchFailed = False
    while expandNode.getState() != goalState1 and expandNode.getState() != goalState2 and not searchFailed:
        visited[expandNode.getState()] = [expandNode.getPath()]
        nodeState = expandNode.getState()
        children.append(moveSpace(nodeState, expandNode.getSpaceLocation(), "Up"))
        children.append(moveSpace(nodeState, expandNode.getSpaceLocation(), "Left"))
        children.append(moveSpace(nodeState, expandNode.getSpaceLocation(), "Down"))
        children.append(moveSpace(nodeState, expandNode.getSpaceLocation(), "Right"))
        for el in children:
            if el[0] == True:
                temppath = expandNode.getPath()
                temppath.append(el[1])
                if expandNode.getDepth() + 1<=maxdepth:
                    stack.append(TreeSearchNode(expandNode, temppath, el[1], expandNode.getDepth() + 1))
                    stats[1] += 1
        stats[2] += 1
        if len(stack) > stats[3]:
            stats[3] = len(stack)
        if(stack != []):
            while(expandNode.getState() in visited):
                expandNode = stack.pop()
        else:
            searchFailed = True
        children.clear()
    if not searchFailed:
        stats[0] = expandNode.getDepth()
        print("Goal State Found!")
        print("Path to goal state:")
        printSolution(expandNode.getPath(), stats)
        return True
    elif limited:
        print("Search Failed!")
    else:
        return False
     


def dfs(puzzle: str, stats):
    if dls(puzzle, stats, 20, false)



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
    moved = "".join(moved)
    return moved

def isSolveable(puzzle: str) -> bool:#check if the given puzzle is solveable
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
        if a>0 and intcpy[a] > 1:
            for num in intcpy[0:a]:
                if num<intcpy[a] and num!=0:
                    inversioncnt -= 1
        elif intcpy[a] == 0:
            inversioncnt+=1

    solveable = False;
    if (0<=emptyidx<=3 or 8<=emptyidx<=11) and inversioncnt % 2 == 1:
        solveable = True
    elif (4<=emptyidx<=7 or 12<=emptyidx<=15) and inversioncnt % 2 == 0:
        solveable = True
    return solveable

def printSolution(path:[str], stats):
    cnt = 0
    if path != []: #check if list is empty, empty lists have a default false value
        for el in path:
            print("State: %d" % (cnt))
            str = "---------------\n|" + " | ".join(el[0:4]) + "|\n---------------\n|" + " | ".join(el[4:8])
            str += "|\n---------------\n|" + " | ".join(el[8:12]) + "|\n---------------\n|" + " | ".join(el[12:16]) + "|\n---------------\n"
            print(str)
            print("\n_________________________\n")
            cnt += 1
    print("Depth: %d  |  Created: %d  |  Expanded: %d  |  Fringe: %d" % (stats[0],stats[1],stats[2],stats[3]))


        
            
'''if __name__ == "__main__":
    main()'''
dls("12345 7896ABDEFC", [0,0,0,1], -1, False)


