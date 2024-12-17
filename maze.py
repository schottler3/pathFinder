import random
from structures import Node, Graph

class Maze:

    def __init__(self, graph):
        self.graph = graph

    def generate(self):
        """
        Generate a maze using backtracking algorithm.
        """
        # Mark all nodes as walls (closed)
        for row in self.graph.nodes:
            for node in row:
                node.open = False
        
        # Choose a random starting cell (must be odd coordinates)
        start_x = random.choice(range(1, self.graph.size, 2))
        start_y = random.choice(range(1, self.graph.size, 2))
        
        # First cell becomes a path
        start_node = self.graph.nodes[start_x][start_y]
        start_node.open = True
        
        # First open cell
        open_cells = [start_node]
        
        while open_cells:
            # Add unnecessary element for code elegance
            open_cells.append(None)
            
            # Find a cell with available neighbors
            while open_cells:
                open_cells.pop()
                if not open_cells:
                    break
                
                cell = open_cells[-1]
                n = self.graph.mazeExpand(cell)
                
                if n:
                    break
            
            # If no more cells, maze generation is complete
            if not open_cells:
                break
            
            # Choose a random neighbor
            choice = random.choice(n)
            open_cells.append(choice)
            
            # Set neighbor to path
            # Set connecting node between cell and choice to path
            choice.open = True
            
            # Find and open the connecting node
            connect_x = (choice.x + cell.x) // 2
            connect_y = (choice.y + cell.y) // 2
            connecting_node = self.graph.nodes[connect_x][connect_y]
            connecting_node.open = True
        
        # Optional: create entrance and exit
        suggestedStart = random.choice(random.choice(self.graph.nodes))
        suggestedGoal = random.choice(random.choice(self.graph.nodes))
        while not suggestedStart.open:
            suggestedStart = random.choice(random.choice(self.graph.nodes))
        while not suggestedGoal.open:
            suggestedGoal = random.choice(random.choice(self.graph.nodes))

        self.graph.start = suggestedStart
        self.graph.goals.append(suggestedGoal)

        return self.graph


