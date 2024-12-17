import random
import time
from flask import Flask, send_file, render_template, abort, request, jsonify # type: ignore
import os
from maze import Maze
from structures import *
from search import Search

app = Flask(__name__)

size = 20

search = Search()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate():
    graph = Graph(size)
    for row in graph.nodes:
        for node in row:
            node.open = False
    graph = Maze(graph).generate()

    return jsonify({'status': 'success', 'maze': graph.to_dict()})

@app.route('/search/<algorithm>', methods=['POST'])
def search_algorithm(algorithm):
    graph = Graph(size)
    data = request.get_json()
    start = data.get('start')
    print(start)
    graph.setStart(int(start.split('-')[0]), int(start.split('-')[1]))

    goals = data.get('goals')
    print(goals)
    for goal in goals:
        x, y = goal.split('-')
        graph.addGoal(int(x), int(y))

    blocks = data.get('walls')
    print(blocks)
    for block in blocks:
        x, y = block.split('-')
        graph.setOpen(int(x), int(y), False)
        print(f"Block: {x}, {y}")

    if algorithm == 'BFS':
        node, steps, shortest = search.BFS(graph)
    elif algorithm == 'DFS':
        node, steps, shortest = search.DFS(graph)
    elif algorithm == 'BestFS':
        node, steps, shortest = search.BestFS(graph)
    elif algorithm == 'A':
        node, steps, shortest = search.A(graph)
    elif algorithm == 'Dijkstra':
        node, steps, shortest = search.Dijkstra(graph)
    elif algorithm == 'BestFSEuclidean':
        node, steps, shortest = search.BestFS(graph, 'euclidean')
    elif algorithm == 'AEuclidean':
        node, steps, shortest = search.A(graph, 'euclidean')
    else:
        return jsonify({'status': 'failure', 'message': 'Unknown algorithm'}), 400

    if node is None:
        return jsonify({'status': 'failure', 'steps': steps})
    else:
        return jsonify({'status': 'success', 'steps': steps, 'shortest': shortest})
    
@app.route('/run', methods=['POST'])
def run():

    csv = open('results5.csv', 'w')
    csv.write('Algorithm,Time,Steps,Length\n')

    for _ in range(100):
        graph = Graph(size)
        for row in graph.nodes:
            for node in row:
                node.open = False
        graph = Maze(graph).generate()

        startBFS = time.time()
        _, stepsBFS, shortestBFS = search.BFS(graph)
        endBFS = time.time()

        startDFS = time.time()
        _, stepsDFS, shortestDFS = search.DFS(graph)
        endDFS = time.time()

        startBestFS = time.time()
        _, stepsBestFS, shortestBestFS = search.BestFS(graph)
        endBestFS = time.time()

        startA = time.time()
        _, stepsA, shortestA = search.A(graph)
        endA = time.time()

        startDijkstra = time.time()
        _, stepsDijkstra, shortestDijkstra = search.Dijkstra(graph)
        endDijkstra = time.time()

        startBestFSEuclidean = time.time()
        _, stepsBestFSEuclidean, shortestBestFSEuclidean = search.BestFS(graph, 'euclidean')
        endBestFSEuclidean = time.time()

        startAEuclidean = time.time()
        _, stepsAEuclidean, shortestAEuclidean = search.A(graph, 'euclidean')
        endAEuclidean = time.time()

        csv.write(f'BFS,{round((endBFS - startBFS) * 1000, 2)},{len(stepsBFS)},{len(shortestBFS)}\n')
        csv.write(f'DFS,{round((endDFS - startDFS) * 1000, 2)},{len(stepsDFS)},{len(shortestDFS)}\n')
        csv.write(f'BestFS,{round((endBestFS - startBestFS) * 1000, 2)},{len(stepsBestFS)},{len(shortestBestFS)}\n')
        csv.write(f'A,{round((endA - startA) * 1000, 2)},{len(stepsA)},{len(shortestA)}\n')
        csv.write(f'Dijkstra,{round((endDijkstra - startDijkstra) * 1000, 2)},{len(stepsDijkstra)},{len(shortestDijkstra)}\n')
        csv.write(f'BestFS Euclidean,{round((endBestFSEuclidean - startBestFSEuclidean) * 1000, 2)},{len(stepsBestFSEuclidean)},{len(shortestBestFSEuclidean)}\n')
        csv.write(f'A Euclidean,{round((endAEuclidean - startAEuclidean) * 1000, 2)},{len(stepsAEuclidean)},{len(shortestAEuclidean)}\n')

    csv.close()
    return jsonify({'status': 'success'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1471)