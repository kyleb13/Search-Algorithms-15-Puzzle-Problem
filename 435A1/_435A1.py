#Kyle Beveridge
#TCSS 435 Assignment 1, 4/15/18
#This program solves the 15 puzzle problem with
#multiple different search algorithms


import time
import sys
import queue

#Tree node class, used to represent a node in the state tree
class TreeSearchNode:

    #Initialize a TreeSearchNode
    #in:    newState= the puzzle state of this node
    #       newDepth = the depth of this node in the tree
    #       newParent = the parent node of this node
    #       newPriority = the priority of this node, used by the priority queues in GBFS and A*
    def __init__(self, newState: str = " ", newDepth: int = 0, newParent = None, newPriority:int = 0):
        self.__state = newState
        self.__spaceLocation = self.__state.find(" ")
        self.__depth = newDepth
        self.parent = newParent
        self.priority = newPriority
        self.right = None
        self.down = None
        self.left = None
        self.up = None

    #support comparison for TreeSearchNode objects
    #in:    other: the other object to compare with
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.getState() == other.getState()
    
    #Support less than operations. This is required by priority queues,
    #and only really has meaning in that context
    def __lt__(self, other):
        return self.priority<other.priority
    
    #Return the puzzle state of this node
    def getState(self) -> str:
        copystate = self.__state
        return copystate

    #return the location of the space in the puzzle state of this node
    def getSpaceLocation(self) -> int:
        return self.__spaceLocation

    #return the depth of this node
    def getDepth(self) -> int:
        return self.__depth



#The two valid goal states to reach
goalState1 = "123456789ABCDEF "
goalState2 = "123456789ABCDFE "

def main():
    stats = [0, 0, 1] #statistics to be printed at the end. idx 0 is number created, 
    #idx 1 is num expanded, idx 2 is fringe size
    puzzle = sys.argv[1]
    method = sys.argv[2]
    tree = generateTree(puzzle, 10)#if number of steps to solution is greater than 10, increase this number. Increasing this will increase compute times drastically
    if method == "BFS":
        bfs(tree, stats)
    elif method == "DFS":
        dls(tree, stats, -1, False)
    elif method == "DLS":
        dls(tree, stats, int(sys.argv[3]), True)
    elif method == "GBFS":
        heuristic = 1
        if(sys.argv[3] == "h2"):
            heuristic = 2
        bfs(tree, stats, True, heuristic, "GBFS")
    elif method == "AStar":
        heuristic = 1
        if(sys.argv[3] == "h2"):
            heuristic = 2
        bfs(tree, stats, True, heuristic, "AStar")
    exit()

#Run a breadth first search of the tree. If informed is set to true, this function
#can also do a GBFS or AStar
#in:    head: pointer to the head of the tree
#       stats = array with the statistics of the search
#       informed = whether an informed search is to be performed or not
#       heuristic = the heuristic to be used if search is informed
#       mode = which algorithm to use if search is informed
def bfs(head, stats, informed: bool = False, heuristic = 1, mode = ""):
    print("Searching for solution...")
    visited = {}
    children = []
    q = None
    if informed:
        q = queue.PriorityQueue(-1)
    else: 
        q = queue.Queue(-1)
    expandNode = head
    while expandNode.getState() != goalState1 and expandNode.getState() != goalState2:
        stats[1] += 1
        if expandNode.right != None and expandNode.right.getState() not in visited:
            children.append(expandNode.right)
            stats[0] += 1
        if expandNode.down != None and expandNode.down.getState() not in visited:
            children.append(expandNode.down)
            stats[0] += 1
        if expandNode.left != None and expandNode.left.getState() not in visited:
            children.append(expandNode.left)
            stats[0] += 1
        if expandNode.up != None and expandNode.up.getState() not in visited:
            children.append(expandNode.up)
            stats[0] += 1
        for el in children:
            if informed:
                if heuristic == 1:
                    el.priority = priorityDifference(el)
                else:
                    el.priority = priorityManhatDist(el)
                if mode == "AStar":
                    el.priority += el.getDepth()
            q.put(el)
        if q._qsize() > stats[2]:
            stats[2] = q._qsize()
        expandNode = q.get() 

        children.clear()
    printSolution(expandNode, stats)

#Run a depth limited search of the tree. If limited is set to false, this function
#will perform a depth first search
#in:    head: pointer to the head of the tree
#       stats = array with the statistics of the search
#       maxdepth = depth to search to if search is limited
#       limited = whether or not the depth search is limited
def dls(head, stats, maxdepth: int, limited: bool = True):
    visited = {}
    stack = []
    expandNode = head
    while expandNode.getState() != goalState1 and expandNode.getState() != goalState2:
        if not limited or expandNode.getDepth()<maxdepth:
            stats[1] += 1
            if expandNode.up != None and expandNode.up.getState() not in visited:
                stack.append(expandNode.up)
                stats[0] += 1
            if expandNode.left != None and expandNode.left.getState() not in visited:
                stack.append(expandNode.left)
                stats[0] += 1
            if expandNode.down != None and expandNode.down.getState() not in visited:
                stack.append(expandNode.down)
                stats[0] += 1
            if expandNode.right != None and expandNode.right.getState() not in visited:
                stack.append(expandNode.right)
                stats[0] += 1
            if len(stack) > stats[2]:
                stats[2] = len(stack)
        expandNode = stack.pop()
    printSolution(expandNode, stats)

#calculate the priority of a node based on heuristic 1, the number of misplaced puzzle pieces
def priorityDifference(node):
    state = node.getState()
    priority = 0
    for idx in range(0, len(state)):
        if state[idx] != goalState1[idx] or state[idx] != goalState2[idx]:
            priority += 1
    return priority

#calculate the priority of a node based on heuristic 2, the manhattan distance
def priorityManhatDist(node):
    endpos = 0
    state = node.getState()
    distance = 0
    for idx in range(0, len(state)):
        if(endpos != idx):
            endpos = goalState1.find(state[idx])
            hend = int(endpos/4)
            hstart = int(idx/4)
            horizontal = abs((endpos - (hend * 4)) - (idx - (hstart * 4)))
            distance += horizontal + abs(hend - hstart)
    return distance

#Make the space move a certain direction
#in:    puzzle = the state of the puzzle
#       idx = the index of the whitespace
#       dir = the direction to move in
#
#out: A list with a bool indicating whether the move was successful,
#and a string with the resulting state
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

#swap two characters in a string. Used in moveSpace()
#in:    string = string to swap characters in
#       idx1 and idx2 = index of characters to swap
#
#out: string result of the swap
def swapChars(string: str, idx1, idx2) -> str:
    moved = string
    moved = list(moved) #convert the string to list so elements can be swapped
    temp = moved[idx2]
    moved[idx2] = moved[idx1]
    moved[idx1] = temp
    moved = "".join(moved)
    return moved

#Get the path to the solution from the start state
#in:    endNode = the node where the goal state was found
#out: string with the path to the goal state
def getSolutionPath(endNode) -> str:
    current = endNode
    path = []
    while(current != None):
        path.append(current.getState())
        current = current.parent #use parent to climb up to top depth
    path.reverse()#reverse the array so the path is in the start -> end order
    return "\n".join(path)

#print out info about the solution
def printSolution(node, stats):
    print("Solution Found! Path:")
    print(getSolutionPath(node))
    print("________________")
    print("Depth: %d| Created: %d| Expanded: %d| Fringe: %d" % (node.getDepth(), stats[0], stats[1], stats[2]))

#Pre-generate the tree, to ensure memory useage is under control
def generateTree(initialState: str, depth:int):
    print("Creating Tree...")
    copy = initialState
    expandNode = TreeSearchNode(copy, 0)
    head = expandNode
    expandQueue = []
    while expandNode.getDepth()<depth:
        r = moveSpace(expandNode.getState(), expandNode.getSpaceLocation(), "Right")
        d = moveSpace(expandNode.getState(), expandNode.getSpaceLocation(), "Down")
        l = moveSpace(expandNode.getState(), expandNode.getSpaceLocation(), "Left")
        u = moveSpace(expandNode.getState(), expandNode.getSpaceLocation(), "Up")
        if r[0]:
            rnode = TreeSearchNode(r[1], expandNode.getDepth() + 1, expandNode, 0)
            expandNode.right = rnode
            expandQueue.append(rnode)
        if d[0]:
            dnode = TreeSearchNode(d[1], expandNode.getDepth() + 1, expandNode, 0)
            expandNode.down = dnode
            expandQueue.append(dnode)
        if l[0]:
            lnode = TreeSearchNode(l[1], expandNode.getDepth() + 1, expandNode, 0)
            expandNode.left = lnode
            expandQueue.append(lnode)
        if u[0]:
            unode = TreeSearchNode(u[1], expandNode.getDepth() + 1, expandNode, 0)
            expandNode.up = unode
            expandQueue.append(unode)
        expandNode = expandQueue.pop(0)
    print("Tree Created!")
    return head


        
            
if __name__ == "__main__":
    main()




