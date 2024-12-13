import queue
from structures import Queue, Node, Graph

class Search:
    def BFS(self, graph):
        node = graph.start
        steps = {}
        time = 0

        if graph.isGoal(node):
            steps[time] = {'node': f"{node.x}-{node.y}", 'status': 'goal'}
            return node, steps
        
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
                    steps[time] = {'node': f"{child.x}-{child.y}", 'status': 'goal'}
                    return child, steps
                if child not in reached:
                    print(f"Visited: {child.x}, {child.y}")
                    reached.add(child)
                    frontier.enqueue(child)
                    steps[time] = {'node': f"{child.x}-{child.y}", 'status': 'visited'}
                    time += 1

        return None, steps
    
    def DFS(self, graph):
        node = graph.start
        steps = {}
        time = 0

        if graph.isGoal(node):
            steps[time] = {'node': f"{node.x}-{node.y}", 'status': 'goal'}
            return node, steps
        
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
                    steps[time] = {'node': f"{child.x}-{child.y}", 'status': 'goal'}
                    return child, steps
                if child not in reached:
                    print(f"Visited: {child.x}, {child.y}")
                    reached.add(child)
                    frontier.append(child)
                    steps[time] = {'node': f"{child.x}-{child.y}", 'status': 'visited'}
                    time += 1

        return None, steps

    ## https://www.geeksforgeeks.org/best-first-search-informed-search/
    def BestFS(self, graph):
        pq = queue.PriorityQueue()
        pq.put((graph.manhattan(graph.start), graph.start))
        steps = []
        steps.append({'node': f"{graph.start.x}-{graph.start.y}", 'status': 'start'})
        while not pq.empty():
            _, u = pq.get()
            if graph.isGoal(u):
                steps.append({'node': f"{u.x}-{u.y}", 'status': 'goal'})
                return u, steps
            else:
                for v in graph.expand(u):
                    if not v.visited:
                        v.visited = True
                        pq.put((graph.manhattan(v), v))
                        steps.append({'node': f"{v.x}-{v.y}", 'status': 'visited'})
                u.visited = True
        return None, steps
    
    ## https://www.geeksforgeeks.org/a-search-algorithm/
    def A(self, graph):
        graph.start.g = 0
        graph.start.h = graph.manhattan(graph.start)
        graph.start.f = graph.start.g + graph.start.h

        open = queue.PriorityQueue()
        open.put((graph.start.f, graph.start))
        closed = set()
        steps = []
        steps.append({'node': f"{graph.start.x}-{graph.start.y}", 'status': 'start'})
        
        while not open.empty():
            _, q = open.get()
            closed.add(q)
            
            for child in graph.expand(q):
                child.parent = q
                if graph.isGoal(child):
                    steps.append({'node': f"{child.x}-{child.y}", 'status': 'goal'})
                    return child, steps
                
                child.g = q.g + 1
                child.h = graph.manhattan(child)
                child.f = child.g + child.h
                
                if any(node for node in open.queue if node[1].x == child.x and node[1].y == child.y and node[1].f <= child.f):
                    continue
                
                if any(node for node in closed if node.x == child.x and node.y == child.y and node.f <= child.f):
                    continue
                
                open.put((child.f, child))
                steps.append({'node': f"{child.x}-{child.y}", 'status': 'visited'})
    
        return None, steps

