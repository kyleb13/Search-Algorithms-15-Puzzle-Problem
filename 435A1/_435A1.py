import time
import sys
import queue

class TreeSearchNode:

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

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.getState() == other.getState()

    def __lt__(self, other):
        return self.priority<other.priority
    
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
    stats = [0, 0, 1] #statistics to be printed at the end. idx 0 is number created, 
    #idx 1 is num expanded, idx 2 is fringe size
    puzzle = sys.argv[1]
    method = sys.argv[2]
    if method == "BFS":
        bfs(puzzle)
    exit()

def bfs(head, stats, informed: bool = False, heuristic = 1, mode = ""):
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
    print("Solution Path:")
    print(getSolutionPath(expandNode))
    print("________________")
    print("Depth: %d| Created: %d| Expanded: %d| Fringe: %d" % (expandNode.getDepth(), stats[0], stats[1], stats[2]))

def dls(head, stats, maxdepth: int, limited: bool = True):
    visited = {}
    stack = []
    expandNode = head
    while expandNode.getState() != goalState1 and expandNode.getState() != goalState2:
        if not limited or expandNode.getDepth()<=maxdepth:
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
    print("Solution Path:")
    print(getSolutionPath(expandNode))
    print("________________")
    print("Depth: %d| Created: %d| Expanded: %d| Fringe: %d" % (expandNode.getDepth(), stats[0], stats[1], stats[2]))

def dfs(head, stats):
    dls(head, stats, 0, False)

def priorityDifference(node):
    state = node.getState()
    priority = 0
    for idx in range(0, len(state)):
        if state[idx] != goalState1[idx] or state[idx] != goalState2[idx]:
            priority += 1
    return priority

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

def getSolutionPath(endNode) -> str:
    current = endNode
    path = []
    while(current != None):
        path.append(current.getState())
        current = current.parent
    path.reverse()
    return "\n".join(path)

def generateTree(initialState: str, depth:int):
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
    return head


        
            
"""if __name__ == "__main__":
    main()"""
print("creating tree....")
tree = generateTree("2 34167859ABDEFC", 10)
print("tree complete!")
dls(tree, [0,0,1], -1, False)
#q = queue.PriorityQueue(-1)
#q.put(TreeSearchNode("Hello", 0, None, 0))
#print(q.get().getState())



