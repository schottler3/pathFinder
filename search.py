import queue
from structures import Queue, Node, Graph

class Search:

    def BFS(self, graph):
        node = graph.start
        steps = {}
        time = 0

        if graph.isGoal(node):
            steps[time] = {'node': f"{node.x}-{node.y}", 'status': 'goal'}
            return node, steps, self.construct_path(node)
        
        frontier = Queue()
        reached = set()
        reached.add(node)
        steps[time] = {'node': f"{node.x}-{node.y}", 'status': 'start'}
        frontier.enqueue(node)
        time += 1

        while not frontier.isEmpty():
            node = frontier.dequeue()
            for child in graph.expand(node):
                if graph.isGoal(child):
                    child.parent = node
                    steps[time] = {'node': f"{child.x}-{child.y}", 'status': 'goal'}
                    return child, steps, self.construct_path(child)
                if child not in reached:
                    print(f"Visited: {child.x}, {child.y}")
                    reached.add(child)
                    child.parent = node
                    frontier.enqueue(child)
                    steps[time] = {'node': f"{child.x}-{child.y}", 'status': 'visited'}
                    time += 1

        return None, steps, None

    def construct_path(self, node):
        path = []
        while node:
            print(f"Tracing path: {node.x}, {node.y}")  # Debug statement
            path.append({'node': f"{node.x}-{node.y}", 'status': 'path'})
            node = node.parent
        path.reverse()
        return path
    
    def DFS(self, graph):
        node = graph.start
        steps = {}
        time = 0

        if graph.isGoal(node):
            steps[time] = {'node': f"{node.x}-{node.y}", 'status': 'goal'}
            return node, steps, self.construct_path(node)
        
        frontier = []
        reached = set()
        reached.add(node)
        steps[time] = {'node': f"{node.x}-{node.y}", 'status': 'start'}
        frontier.append(node)
        time += 1

        while frontier:
            node = frontier.pop()
            for child in graph.expand(node):
                if graph.isGoal(child):
                    child.parent = node
                    steps[time] = {'node': f"{child.x}-{child.y}", 'status': 'goal'}
                    return child, steps, self.construct_path(child)
                if child not in reached:
                    print(f"Visited: {child.x}, {child.y}")
                    reached.add(child)
                    child.parent = node
                    frontier.append(child)
                    steps[time] = {'node': f"{child.x}-{child.y}", 'status': 'visited'}
                    time += 1

        return None, steps, []

    ## https://www.geeksforgeeks.org/best-first-search-informed-search/
    def BestFS(self, graph, algorithm='manhattan'):
        pq = queue.PriorityQueue()
        pq.put((getattr(graph,algorithm)(graph.start), graph.start))
        steps = []
        steps.append({'node': f"{graph.start.x}-{graph.start.y}", 'status': 'start'})
        reached = set()
        reached.add(graph.start)
        
        while not pq.empty():
            _, u = pq.get()
            if graph.isGoal(u):
                steps.append({'node': f"{u.x}-{u.y}", 'status': 'goal'})
                return u, steps, self.construct_path(u)
            else:
                for v in graph.expand(u):
                    if v not in reached:
                        reached.add(v)
                        v.parent = u
                        pq.put((getattr(graph,algorithm)(v), v))
                        steps.append({'node': f"{v.x}-{v.y}", 'status': 'visited'})
                u.visited = True
        return None, steps, []
    
    ## https://www.geeksforgeeks.org/a-search-algorithm/
    def A(self, graph, algorithm='manhattan'):
        # Initialize all nodes
        for row in graph.nodes:
            for node in row:
                node.g = float('inf')
                node.h = 0
                node.f = float('inf')
        
        graph.start.g = 0
        graph.start.h = float(getattr(graph, algorithm)(graph.start))  # Convert to float
        graph.start.f = graph.start.g + graph.start.h

        open = queue.PriorityQueue()
        # Add node ID as tiebreaker
        open.put((graph.start.f, id(graph.start), graph.start))
        closed = set()
        steps = []
        steps.append({'node': f"{graph.start.x}-{graph.start.y}", 'status': 'start'})
        
        while not open.empty():
            _, _, q = open.get()
            # ...existing code...
            for child in graph.expand(q):
                if child in closed:
                    continue
                
                tentative_g = float(q.g + 1)  # Convert to float
                if tentative_g < child.g:
                    child.parent = q
                    child.g = tentative_g
                    child.h = float(getattr(graph, algorithm)(child))  # Convert to float
                    child.f = child.g + child.h
                    
                    if graph.isGoal(child):
                        steps.append({'node': f"{child.x}-{child.y}", 'status': 'goal'})
                        return child, steps, self.construct_path(child)
                    
                    open.put((child.f, id(child), child))
                    steps.append({'node': f"{child.x}-{child.y}", 'status': 'visited'})
        
        return None, steps, []

    def Dijkstra(self, graph):
        sptSet = set()
        steps = []
        
        # Initialize distances
        for row in graph.nodes:
            for node in row:
                node.g = float('inf')
                node.parent = None
        graph.start.g = 0

        total_nodes = sum(len(row) for row in graph.nodes)

        while len(sptSet) != total_nodes:
            u = self.minDistance(graph, sptSet)
            if u is None:
                break
                
            steps.append({'node': f"{u.x}-{u.y}", 'status': 'visited'})
            sptSet.add(u)

            # Check if current node is goal
            if graph.isGoal(u):
                return u, steps, self.construct_path(u)

            for v in graph.expand(u):
                if v not in sptSet and u.g + 1 < v.g:
                    v.g = u.g + 1
                    v.parent = u
                    steps.append({'node': f"{v.x}-{v.y}", 'status': 'updated'})

        return None, steps, []

    def minDistance(self, graph, sptSet):
        min_dist = float('inf')
        min_node = None

        for row in graph.nodes:
            for node in row:
                if node not in sptSet and node.g < min_dist:
                    min_dist = node.g
                    min_node = node

        return min_node