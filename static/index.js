const gridSize = 20;
let start;
let algorithm = 'BFS';
let goals = [];
let cells = [];
let blocks = [];
let mousedown = false;
let editing = true;

let populateGrid = function() {
    let grid = document.getElementById('grid');
    for (let i = 0; i < gridSize; i++) {
        let row = document.createElement('div');
        row.className = 'row';
        grid.appendChild(row);
        for(let j = 0; j < gridSize; j++) {
            let cell = document.createElement('div');
            cell.className = 'cell';
            cell.id = i + '-' + j;
            cell.state = 0;
            cells.push(cell);
            cell.addEventListener('click', function(event) {
                switch(cell.state){
                    case 0:
                        cell.style.backgroundColor = 'black';
                        cell.state = 1;
                        blocks.push(cell.id);
                        break;
                    case 1:
                        cell.style.backgroundColor = 'green';
                        cell.state = 2;
                        blocks.splice(blocks.indexOf(cell.id), 1);
                        goals.push(cell);
                        break;
                    case 2:
                        if(start){
                            start.style.backgroundColor = 'white';
                            start.state = 0;
                        }
                        if (goals.includes(cell)){
                            let index = goals.indexOf(cell);
                            goals.splice(index, 1);
                        }
                        cell.style.backgroundColor = 'red';
                        cell.state = 3;
                        start = cell;
                        break;
                    case 3:
                        cell.style.backgroundColor = 'white';
                        if(start == cell){
                            start = null;
                        }
                        cell.state = 0;
                        break;
                }

            });
            cell.addEventListener('mousedown', function() {
                mousedown = true;
            });
            cell.addEventListener('mouseup', function() {
                mousedown = false;
            });
            cell.addEventListener('mouseenter', function() {
                if(mousedown){
                    cell.style.backgroundColor = 'black';
                    if(cell.state == 2){
                        goals.splice(goals.indexOf(cell), 1);
                    }
                    else if(cell.state == 3){
                        start = null;
                    }
                    blocks.push(cell.id);
                    cell.state = 1;
                }
            });
            row.appendChild(cell);
        }
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

let displayPath = async function(steps) {
    let grid = document.getElementById('grid');
    let sortedSteps = Object.keys(steps).sort((a, b) => a - b).map(key => steps[key]);

    for (let step of sortedSteps) {
        let cell = document.getElementById(step.node);
        if(cell.state == 2){
            cell.style.backgroundColor = 'darkgreen';
        }
        else if(cell.state == 3){
            cell.style.backgroundColor = 'darkred';
        }
        else
            if(step.status == 'visited')
                cell.style.backgroundColor = 'blue';
            else if (step.status == 'updated')
                cell.style.backgroundColor = 'yellow';
        await sleep(10);
    }
}

let displayShortest = async function(steps) {
    let sortedSteps = Object.keys(steps).sort((a, b) => a - b).map(key => steps[key]);

    for (let step of sortedSteps) {
        let cell = document.getElementById(step.node);
        if(cell.state == 2){
            cell.style.backgroundColor = 'darkgreen';
        }
        else if(cell.state == 3){
            cell.style.backgroundColor = 'darkred';
        }
        else
            cell.style.backgroundColor = 'aqua';
        await sleep(10);
    }
}
    

let setAlgorithm = function(algo) {
    algorithm = algo;
}

let search = function() {
    switch(algorithm){
        case 'BFS':
            searchFetch('BFS');
            break;
        case 'DFS':
            searchFetch('DFS');
            break;
        case 'BestFS':
            searchFetch('BestFS');
            break;
        case 'A':
            searchFetch('A');
            break;
        case 'Dijkstra':
            searchFetch('Dijkstra');
            break;
        case 'BestFSEuclidean':
            searchFetch('BestFSEuclidean');
            break;
        case 'AEuclidean':
            searchFetch('AEuclidean');
            break;
    }
}

let searchFetch = async function(algorithm) {
    console.log(goals);
    console.log(start);
    editing = false;

    let gridData = {
        start: start.id,
        goals: goals.map((goal) => goal.id),
        walls: blocks
    }
    
    response = await fetch(`/search/${algorithm}`, {
        method: 'POST',
        body: JSON.stringify(gridData),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if(response.ok){
        let data = await response.json();
        console.log(data);
        await displayPath(data.steps);
        if(data.shortest){
            displayShortest(data.shortest);
        }
        editing = true;
    }
}

let runTest = async function() {
    response = await fetch(`/run`, {
        method: 'POST',
    })

    if(response.ok){
        let data = await response.json();
        console.log(data);
    }
}


let setGrid = async function() {
    clearGrid();
    response = await fetch(`/generate`, {
        method: 'GET',
    })

    if(response.ok){
        console.log('Grid set');
        let data = await response.json();
        console.log(data);
        if(data.maze && data.maze.nodes){
            // Iterate through the nodes array
            data.maze.nodes.forEach(row => {
                row.forEach(node => {
                    let cell = document.getElementById(node.id);
                    if(cell) {
                        if(!node.open) {
                            cell.style.backgroundColor = 'black';
                            cell.state = 1;
                            blocks.push(cell.id);
                        }
                        else {
                            cell.style.backgroundColor = 'white';
                            cell.state = 0;
                        }
                }
            });
        });
        let GenStart = document.getElementById(data.maze.start.id);
        GenStart.style.backgroundColor = 'red';
        GenStart.state = 3;
        start = GenStart;
        goals = [];
        for(let goal of data.maze.goals){
            let cell = document.getElementById(goal.id);
            cell.style.backgroundColor = 'green';
            cell.state = 2;
            goals.push(cell);
        }
    } else {
        console.log('No maze data');
    }
  }
}

let clearGrid = function() {
    for(let cell of cells){
        cell.style.backgroundColor = 'white';
        cell.state = 0;
    }
    blocks = [];
    goals = [];
    start = null;
}


window.onload = function() {
    populateGrid();
}