class Node:
    def __init__(self, x, y, open):
        self.x = x
        self.y = y
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.open = open
        self.visited = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

class Graph:
    def __init__(self, size):
        self.size = size
        self.nodes = []
        self.goals = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(Node(i, j, True))
            self.nodes.append(row)

    def setOpen(self, x, y, open):
        self.nodes[x][y].open = open

    def addGoal(self, x, y):
        self.goals.append(self.nodes[x][y])

    def setStart(self, x, y):
        self.start = self.nodes[x][y]

    def expand(self, node):
        actions = []
        x = node.x
        y = node.y
        nodes = self.nodes
        if y + 1 < self.size and nodes[x][y + 1].open:
            actions.append(nodes[x][y + 1])
        if x + 1 < self.size and nodes[x + 1][y].open:
            actions.append(nodes[x + 1][y])
        if y - 1 >= 0 and nodes[x][y - 1].open:
            actions.append(nodes[x][y - 1])
        if x - 1 >= 0 and nodes[x - 1][y].open:
            actions.append(nodes[x - 1][y])
        return actions

    def isGoal(self, node):
        return node in self.goals
    
    def manhattan(self, node):
        return min(abs(node.x - goal.x) + abs(node.y - goal.y) for goal in self.goals)

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, node):
        self.queue.append(node)

    def dequeue(self):
        return self.queue.pop(0)

    def isEmpty(self):
        return len(self.queue) == 0