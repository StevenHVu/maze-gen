#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
import numpy as np

def initialize_maze(width, height):
    """
    Initializes the maze grid with 1s which represent walls.

    Parameters:
    - width (int): the width of the maze (# of columns)
    - height (int): the height of the maze (# of rows)

    Returns:
    - list of lists: a 2d grid that represents the maze, with each cell being initialized with 1, indicating a wall

    Example:
    - initialize_maze(11, 11) # returns a 11x11 grid filled with 1s
    """
    
    # ensure dimensions are odd to allow for proper boundaries
    if width % 2 == 0:
        width += 1  # if width is even, make it odd
    if height % 2 == 0:
        height += 1  # if height is even, make it odd
    
    # return a 2d grid (list of lists) where each cell is initialized to 1 (wall)
    return [[1 for _ in range(width)] for _ in range(height)]

def check_point_condition(point, maze, width, height):
    """
    Checks the surrounding cells of a given point (x, y) to determine how many neighboring walls (1s) exist.

    Parameters:
    - point (tuple): (x, y) coordinates of the current point in the maze
    - maze (list of lists): the 2d grid representing the maze
    - width (int): the width of the maze
    - height (int): the height of the maze

    Returns:
    - int: the number of walls (1s) surrounding the point

    Example:
    - check_point_condition((1, 1), maze, 5, 5) # returns the number of neighboring walls around (1, 1)
    """
    
    x, y = point
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]  # define neighboring cells (left, right, up, down)
    wall_count = 0  # counter for walls surrounding the point

    # iterate through all neighboring cells
    for nx, ny in neighbors:
        # ensure the neighbor is within bounds and check if it's a wall
        if 0 < nx < width and 0 < ny < height:
            if maze[ny][nx] == 1:
                wall_count += 1  # increment wall count if the neighbor is a wall
    
    return wall_count  # return the number of walls surrounding the point

def carve_maze(start, end, maze, width, height):
    """
    Carves paths into the maze grid using Depth-First Search (DFS).
    Randomly shuffles directions to create randomized maze patterns.
    Directions have a magnitude of 2, allowing more walls between paths.

    Parameters:
    - start (tuple): (x, y) coordinates of the starting point in the maze
    - end (tuple): (x, y) coordinates of the end point in the maze
    - maze (list of lists): a 2d grid where cells are 0 (for path) or 1 (for wall)
    - width (int): the width of the maze
    - height (int): the height of the maze

    Modifies:
    - maze: the maze grid is modified by carving paths (set cells to 0)

    Example:
    - carve_maze((1, 1), (3, 3), maze, 8, 8)
    """
    
    stack = [start]  # start with the initial position in the stack
    maze[start[0]][start[1]] = 0  # mark the starting point as part of the path

    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # down, right, up, left (steps of 2 to leave walls in between)

    # if the end-point is still a wall, carve it into a path
    if maze[end[0]][end[1]] == 1:
        maze[end[0]][end[1]] = 0

    # continue until the stack is empty (backtrack when no valid moves are found)
    while stack:
        current_x, current_y = stack[-1]  # get the current position from the stack
        random.shuffle(directions)  # shuffle directions to randomize path carving
        
        carved = False  # flag to check if a new path was carved
        for dx, dy in directions:  # iterate through all four directions
            nx, ny = current_x + dx, current_y + dy  # calculate the new position of the cell

            # check if the new position is within bounds and is a wall
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                maze[current_y + dy // 2][current_x + dx // 2] = 0  # carve the wall between current and new position
                maze[ny][nx] = 0  # mark the new position as part of the path
                stack.append((nx, ny))  # add the new position to the stack
                carved = True
                break  # stop after carving one direction
        
        if not carved:  # if no valid move is found, backtrack by popping the stack
            stack.pop()

    # make sure the endpoint is connected to the maze
    if check_point_condition != 3:
        random.shuffle(directions)  # shuffle directions for randomness
        for dx, dy in directions:
            nx, ny = end[1] + dx, end[0] + dy  # check surrounding cells of the endpoint
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 0:
                maze[end[0] + dy // 2][end[1] + dx // 2] = 0  # carve the wall between current and new position

def generate_maze(start, end, width, height):
    """
    Generates a complete maze by initializing the grid and carving paths.

    Parameters:
    - start (tuple): (x, y) coordinates of the starting point in the maze
    - end (tuple): (x, y) coordinates of the end point in the maze
    - width (int): the width of the maze
    - height (int): the height of the maze

    Returns:
    - maze (list of lists): a 2d grid where cells are 0 (for path) or 1 (for wall)

    Example:
    - generate_maze((1, 1), (9, 9), 10, 10)
    """
    
    maze = initialize_maze(width, height)  # create an initialized maze
    carve_maze(start, end, maze, width, height)  # carve the paths into the maze
    return maze  # return the generated maze

def dijkstra(start, end, maze, width, height):
    """
    Implements Dijkstra's algorithm to find the shortest path from start to end in the maze.

    Parameters:
    - start (tuple): (x, y) coordinates of the starting point
    - end (tuple): (x, y) coordinates of the end point
    - maze (list of lists): a 2d grid representing the maze
    - width (int): the width of the maze
    - height (int): the height of the maze

    Returns:
    - distances (dict): a dictionary with coordinates as keys and the shortest distance from start as values
    - path (list): a list of coordinates representing the shortest path from start to end

    Example:
    - dijkstra((1, 1), (9, 9), maze, 10, 10)
    """
    
    distances = {}  # dictionary to store distances from start to each point
    visited = {}    # dictionary to track visited points
    predecessors = {}  # dictionary to store the predecessors for path reconstruction

    # initialize distances for all path cells to infinity and mark them as unvisited
    for x in range(height):
        for y in range(width):
            if maze[x][y] == 0:  # only consider path cells (0)
                distances[(x, y)] = float('inf')  # set initial distances to infinity
                visited[(x, y)] = False  # mark all path cells as unvisited

    distances[start] = 0  # starting point has distance 0
    predecessors[start] = None  # no predecessor for the start point

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up (grid movements)

    while True:
        min_distance = float('inf')  # start with a very large minimum distance
        unvisited = None  # variable to store the unvisited cell with the smallest distance

        # iterate through all cells to find the unvisited cell with the smallest distance
        for cell, distance in distances.items():
            if not visited[cell] and distance < min_distance:
                min_distance = distance
                unvisited = cell

        if unvisited is None:  # if no unvisited cell is found, break (all reachable cells are visited)
            break

        visited[unvisited] = True  # mark the current cell as visited
        ux, uy = unvisited  # extract the coordinates of the current cell

        # update distances for neighboring cells (adjacent cells)
        for dx, dy in directions:
            nx, ny = ux + dx, uy + dy  # calculate the coordinates of neighboring cells
            if (nx, ny) in distances and not visited[(nx, ny)]:  # if the neighbor is a valid path cell
                alt = distances[unvisited] + 1  # calculate the alternate distance
                if alt < distances[(nx, ny)]:  # if the new distance is shorter, update it
                    distances[(nx, ny)] = alt
                    predecessors[(nx, ny)] = unvisited  # update the predecessor for path reconstruction

    # reconstruct the shortest path from end to start by following the predecessors
    path = []
    current = end
    while current is not None:
        path.append(current)  # add the current cell to the path
        current = predecessors.get(current)  # move to the predecessor
    path.reverse()  # reverse the path to get it from start to end
    
    return distances, path  # return the distances dictionary and the shortest path

def visualize_maze(maze, width, height, shortest_path, distances, show_distances_flag='1'):
    """
    Visualizes the maze and overlays the shortest path and distance values.

    Parameters:
    - maze (list of lists): a 2d grid representing the maze
    - width (int): the width of the maze
    - height (int): the height of the maze
    - shortest_path (list): a list of coordinates representing the shortest path
    - distances (dict): a dictionary with coordinates as keys and distances as values

    Example:
    - visualize_maze(maze, 10, 10, shortest_path, distances)
    """
    
    maze_with_path = [row[:] for row in maze]  # create a copy of the maze to overlay the shortest path
    for x, y in shortest_path:
        maze_with_path[x][y] = 2  # mark the shortest path with a special value (2)

    maze_array = np.array(maze_with_path)  # convert the maze to a numpy array for visualization

    # define a colormap: white for paths, black for walls, red for the shortest path
    cmap = plt.cm.colors.ListedColormap(['white', 'black', 'red'])

    plt.imshow(maze_array, cmap=cmap, origin="upper")  # display the maze

    # dynamically determine font size based on the maze size
    fontsize = min(18, 250 // max(height, width))
    print(f"fontsize: ", fontsize)

    if show_distances_flag:
        # overlay distance values on the path and shortest path cells
        for x in range(height):
            for y in range(width):
                if maze[x][y] == 0 or maze_with_path[x][y] == 2:  # check if it's part of the path
                    if (x, y) in distances:  # check if the distance is available
                        dist_value = distances[(x, y)]  # get the distance
                        if dist_value < float('inf'):  # avoid infinite distances
                            color = "black" if maze_with_path[x][y] != 2 else "white"  # choose text color
                            plt.text(y, x, f"{dist_value:.0f}", ha='center', va='center', fontsize=fontsize, color=color)
        
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(18, 10)
    plt.axis('off')
    plt.show()  # display the plot

def main():
    user_input = input ("Enter '0' for default small maze, '1' for default large maze, '2' for custom maze: ")
    if user_input == '0':
        width = 11
        height = 11
        start = (1, 1)
        end = (height - 2, width - 2)

        maze = generate_maze(start, end, width, height)
        distances, shortest_path = dijkstra(start, end, maze, width, height)
        visualize_maze(maze, width, height, shortest_path, distances)
    if user_input == '1':
        width = 50
        height = 50
        start = (1, 1)
        end = (height - 1, width - 1)

        maze = generate_maze(start, end, width, height)
        distances, shortest_path = dijkstra(start, end, maze, width, height)
        visualize_maze(maze, width, height, shortest_path, distances)
    elif user_input == '2':
        width = int(input("Enter width value: "))
        height = int(input("Enter height value: "))
        start_x = int(input("Enter starting x-coordinate: "))
        start_y = int(input("Enter starting y-coordinate: "))
        start = (start_y, start_x)
        end_x = int(input("Enter end point x-coordinate: "))
        end_y = int(input("Enter end point y-coordinate: "))
        end = (end_x, end_y)
        
        show_distances_flag = int(input("Would you like to display the distances from the source on every path cell? Enter '0' for no display."))
        maze = generate_maze(start, end, width, height)
        distances, shortest_path = dijkstra(start, end, maze, width, height)
        visualize_maze(maze, width, height, shortest_path, distances, show_distances_flag)
    else: 
        print(f"Please enter a valid, positive integer into these fields and try again.")

if __name__ == "__main__":
    main()