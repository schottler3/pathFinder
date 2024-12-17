class Node:
    def __init__(self, x, y, open):
        self.x = x
        self.y = y
        self.g = float('inf')
        self.h = 0
        self.open = open
        self.visited = False
        self.parent = None 

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
    
    def to_dict(self):
        return {
            'id': str(self.x) + '-' + str(self.y),
            'open': self.open,
        }

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
    
    def mazeExpand(self, node):
        actions = []
        x = node.x
        y = node.y
        nodes = self.nodes
        # Check for walls (not open) that are 2 cells away
        if y + 2 < self.size and not nodes[x][y + 2].open:
            actions.append(nodes[x][y + 2])
        if x + 2 < self.size and not nodes[x + 2][y].open:
            actions.append(nodes[x + 2][y])
        if y - 2 >= 0 and not nodes[x][y - 2].open:
            actions.append(nodes[x][y - 2])
        if x - 2 >= 0 and not nodes[x - 2][y].open:
            actions.append(nodes[x - 2][y])
        return actions

    def isGoal(self, node):
        return node in self.goals
    
    def manhattan(self, node):
        return min(abs(node.x - goal.x) + abs(node.y - goal.y) for goal in self.goals)
    
    def cost(self, node1, node2):
        return 1
    
    def to_dict(self):
        return {
            'size': self.size,
            'nodes': [[node.to_dict() for node in row] for row in self.nodes],
            'goals': [goal.to_dict() for goal in self.goals],
            'start': self.start.to_dict(),
        }

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, node):
        self.queue.append(node)

    def dequeue(self):
        return self.queue.pop(0)

    def isEmpty(self):
        return len(self.queue) == 0