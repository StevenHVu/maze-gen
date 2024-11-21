# Maze Generator and Solver

## Description
A program that generates random mazes and finds the shortest path to navigate through them.

### Maze Generation
The maze will be represented as a 2D grid in which each cell is either traversible (paths) or not traversible (walls). The maze will be generated or "carved" using a Depth-First Search (DFS) algorithm.

### Pathfinding and Maze Solving
Calculation of the shortest path is done using Dijikstra's Algorithm with the path being determined by looping through a cell's predecessor.

### Generation Options & User Interaction
The user has some options for generating the maze which the user can choose during runtime. There's two default sizes: 11x11 and 51x51, and a customized maze option which allows the user enter in their parameters like width, height, starting, and ending points of the maze.

### Visualizatiion
The matplotlib library will be used to display the shortest path solution as well as the distance values of all available cells from the source/starting point.

## How to use
Make the script executable by running this command:
<code>chmod +x maze.py </code>

Run the script:
<code>./maze.py</code>

Alternatively, you can run using Python directly:
<code>python3 maze.py</code>