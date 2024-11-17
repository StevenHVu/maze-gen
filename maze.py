#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
import numpy as np

def initialize_maze(width, height):
    # Functionality:
    # - Initializes the maze grid with 1s which represent walls

    # Parameters:
    # - width (int): the width of the maze (# of columns)
    # - height (int): the height of the maze (# of rows)

    # Returns:
    # - list of lists: a 2d grid that represents the maze, with each cell being initialized with 1, indicating a wall

    # Example:
    # initialize_maze(11, 11) # returns a 11x11 grid filled with 1s
    
    # Ensure dimensions are odd to allow for proper boundaries
    if width % 2 == 0:
        width += 1

    if height % 2 == 0:
        height += 1
    
    return [[1 for _ in range(width)] for _ in range(height)]

def check_point_condition(point, maze, width, height):
    x, y = point
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    wall_count = 0

    for nx, ny in neighbors:
        if 0 < nx < width and 0 < ny < height:
            if maze[ny][nx] == 1:
                wall_count += 1
    
    return wall_count

def carve_maze(start, end, maze, width, height):
    # Functionality
    # - Carves paths into the maze grid using Depth-First Search (DFS)
    # - Randomly shuffles directions to create randomized maze patterns
    # - Directions have a magnitude of 2, allowing more walls between paths

    # Parameters:
    # - maze (list of lists): a 2d grid where cells are 0 (for path) or 1 (for wall)

    # Modifies:
    # - the `maze` grid by marking visited cells as paths (0) 

    # Returns:
    # - None: the function modifies the maze by setting cells as part of the path

    # Example:
    # - carve_maze(1, 1, maze, maze, 8, 8)

    stack = [start]  # start with the initial position in the stack
    maze[start[0]][start[1]] = 0  # mark the starting point as part of the path

    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # down, right, up, left movements

    if maze[end[0]][end[1]] == 1: # mark the end-point as a path
        maze[end[0]][end[1]] = 0  # carve the endpoint if it is still a wall

    while stack:
        current_x, current_y = stack[-1]  # get the current position from the stack
        random.shuffle(directions)  # shuffle directions for randomness
        
        carved = False
        for dx, dy in directions: # iterate through all the directions
            nx, ny = current_x + dx, current_y + dy # calculate the new positions of the cell

            # check if the new position is valid (within bounds and a wall)
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                maze[current_y + dy // 2][current_x + dx // 2] = 0 # carve the wall between the current and new position
                maze[ny][nx] = 0  # mark the new position as part of the path
                stack.append((nx, ny))  # sdd the new position to the stack
                carved = True
                break
        
        if not carved:  # if no valid move is found, backtrack
            stack.pop()

    if check_point_condition != 3:
        random.shuffle(directions)  # shuffle directions for randomness
        for dx, dy in directions:
            nx, ny = end[1] + dx, end[0] + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 0:
                maze[end[0] + dy // 2][end[1] + dx // 2] = 0 # carve the wall between the current and new position
                print(f"Carved")
                break
        print(f"True")

def generate_maze(start, end, width, height):
    # Functionality
    # - Generates a complete maze by initializing the grid and carving paths

    # Parameters
    # - width (int): the width of the maze (# of columns)
    # - height (int): the height of the maze (# of rows)

    # Returns:
    # maze (list of list): a 2d grid where cells are 0 (for path) or 1 (for wall)

    # Example
    # - maze = generate_maze(10, 10)

    maze = initialize_maze(width, height)
    carve_maze(start, end, maze, width, height)
    return maze

def visualize_maze(maze):
    maze_array = np.array(maze)
    plt.imshow(maze_array, cmap="gray_r")
    plt.show()

def main():
    # (y, x)
    while True:
        width = 21
        height = 21
        start = (1, 1)
        # end = (10, 10)
        end = (width - 2, height - 2)

        maze = generate_maze(start, end, width, height)
        visualize_maze(maze)
    # # Customize
    # width = int(input("Enter the width of the maze: "))
    # height = int(input("Enter the height of the maze: "))

    # start_x = int(input("Enter the starting x-coordinate for the maze: "))
    # start_y = int(input("Enter the starting y-coordinate for the maze: "))
    # start = (start_y, start_x)

    # end_x = int(input("Enter the ending x-coordinate for the maze: "))
    # end_y = int(input("Enter the ending y-coordinate for the maze: "))
    # end = (end_y, end_x)

    # maze = generate_maze(start, end, width, height)
    # visualize_maze(maze)

if __name__ == "__main__":
    main()