from flask import Flask, send_file, render_template, abort, request, jsonify
import os
from structures import *
from search import Search

app = Flask(__name__)

size = 16

search = Search()

@app.route('/')
def index():
    return render_template('index.html')

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
        node, steps = search.BFS(graph)
    elif algorithm == 'DFS':
        node, steps = search.DFS(graph)
    elif algorithm == 'BestFS':
        node, steps = search.BestFS(graph)
    elif algorithm == 'A':
        node, steps = search.A(graph)
    else:
        return jsonify({'status': 'failure', 'message': 'Unknown algorithm'}), 400

    if node is None:
        return jsonify({'status': 'failure', 'steps': steps})
    else:
        return jsonify({'status': 'success', 'steps': steps})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1471)