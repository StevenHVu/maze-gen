#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
import numpy as np

# Defines
def initialize_maze(width, height):
    return [[1 for _ in range(width)] for _ in range(height)]

def carve_maze(start_x, start_y, end_x, end_y, maze, width, height):
    stack = [(start_x, start_y)]  # start with the initial position in the stack
    maze[start_y][start_x] = 0  # mark the starting point as part of the path

    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # down, right, up, left movements

    if maze[end_y][end_x] == 1: # mark the end-point as a path
        maze[end_y][end_x] = 0  # carve the endpoint if it is still a wall

    while stack:
        current_x, current_y = stack[-1]  # get the current position from the stack
        random.shuffle(directions)  # shuffle directions for randomness
        
        carved = False
        for dx, dy in directions: # iterate through all the directions
            nx, ny = current_x + dx, current_y + dy # calculate the new positions of the cell

            # check if the new position is valid (within bounds and a wall)
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[current_y + dy // 2][current_x + dx // 2] = 0 # carve the wall between the current and new position
                maze[ny][nx] = 0  # mark the new position as part of the path
                stack.append((nx, ny))  # sdd the new position to the stack
                carved = True
                break
        
        if not carved:  # if no valid move is found, backtrack
            stack.pop()

def generate_maze(start_x, start_y, width, height):
    maze = initialize_maze(width, height)
    carve_maze(start_x, start_y, end_x, end_y, maze, width, height)
    return maze

def visualize_maze(maze):
    maze_array = np.array(maze)
    plt.imshow(maze_array, cmap="gray_r")
    plt.show()

width = int(input("Enter the width (preferably, an odd number) of the maze: "))
height = int(input("Enter the (preferably, an odd number) height of the maze: "))

start_x = int(input("Enter the starting x-coordinate for the maze: "))
start_y = int(input("Enter the starting y-coordinate for the maze: "))

end_x = int(input("Enter the ending x-coordinate for the maze: "))
end_y = int(input("Enter the ending y-coordinate for the maze: "))

maze = generate_maze(start_x, start_y, width, height)

visualize_maze(maze)