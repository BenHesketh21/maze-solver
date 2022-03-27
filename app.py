#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------
import logging
import os
import time

logging.basicConfig(level=logging.CRITICAL)


def find_start_of_maze(maze):
    for row in maze:
        for space in row:
            if space == "O":
                starting_spot = [row.index(space), maze.index(row)]
    return starting_spot

def get_maze_value(space, maze):
    value = maze[space[1]][space[0]]
    logging.debug("Getting value: %s: %r", space, value)
    return value


def is_space_available(space, maze, failed_spaces_list_to_check):
    value = get_maze_value(space, maze)
    logging.debug("%s = %r", space, value)
    if value == " ":
        if not space in failed_spaces_list_to_check:
            return True
    return False

def print_maze(maze):
    maze_to_print = maze.copy()
    for index, row in enumerate(maze_to_print):
        row_to_print = row.copy()
        row_to_print.append("\n")
        maze_to_print[index] = " ".join(row_to_print)
    return "".join(maze_to_print)

def find_adjacent_spaces(space, path):
    adjacent_spaces = []
    adjacent_spaces.append([space[0], space[1] - 1])
    adjacent_spaces.append([space[0] + 1, space[1]])
    adjacent_spaces.append([space[0], space[1] + 1])
    adjacent_spaces.append([space[0] - 1, space[1]])
    logging.debug("All Adjacent Spaces: %s", adjacent_spaces)
    for found_space in adjacent_spaces:
        if found_space[0] < 0 or found_space[1] < 0 or found_space in path or found_space[0] > 8 or found_space[1] > 8:
            adjacent_spaces.pop(adjacent_spaces.index(found_space))
    return adjacent_spaces

def is_maze_solved(current_space, maze, path, solved_paths_to_check):
    adjacent_spaces = find_adjacent_spaces(current_space, path)
    maze_solved = False
    paths_already_solved = [[]]
    for path_and_maze in solved_paths_to_check:
        paths_already_solved.append(path_and_maze[0])
    for side in adjacent_spaces:
        row = maze[side[1]]
        value = row[side[0]]
        if value == "X" and path not in paths_already_solved:
            maze_solved = True
    return maze_solved

def change_value(maze, space, value):
    logging.debug("Maze Type: %s, %r", type(maze), maze)
    logging.debug("Space Type: %s, %r", type(space), space)
    logging.debug("Value Type: %s, %r", type(value), value)
    logging.debug(space)
    logging.debug("Old value Type: %s, %r", type(maze[space[1]][space[0]]), maze[space[1]][space[0]])
    maze[space[1]][space[0]] = value
    logging.debug("New Maze: %s", type(maze))
    logging.debug("New value Type: %s, %r", type(maze[space[1]][space[0]]), maze[space[1]][space[0]])
    return maze

def get_available(list_of_spaces, maze, failed_spaces_list):
    available = []
    logging.debug(f"Failed: {failed_spaces_list}")
    for space in list_of_spaces:
        if is_space_available(space, maze, failed_spaces_list):
            available.append(space)
    return available

def cls(): 
    os.system('clear')

def reset_maze(maze_to_reset):
    for row_index, row in enumerate(maze_to_reset):
        for space_index, space in enumerate(row):
            if space == "x":
                maze = change_value(maze_to_reset, [space_index, row_index], " ")
    return maze



def solve_maze(maze, solved, failed_spaces, starting_point):
    
    path = [starting_point]
    current_space = starting_point
    print("Current", current_space)
    visited_space = "x"
    while not is_maze_solved(current_space, maze, path, solved):
        print(print_maze(maze))
        time.sleep(0.25)
        available_next_spaces = find_adjacent_spaces(current_space, path)
        logging.info("Current: %s", current_space)
        logging.info("Adjacent Next: %s", available_next_spaces)
        available_spaces = get_available(available_next_spaces, maze, failed_spaces)
        logging.info("Available Next: %s", available_spaces)
        if len(available_spaces) == 0:
            if len(failed_spaces) > 5:
                failed_spaces.pop(0)
            failed_spaces.append(current_space)
            path.pop(path.index(current_space))
            maze = change_value(maze, current_space, " ")
            current_space = path[-1]
        else:
            next_space = available_spaces[0]
            logging.info("Going to %s", next_space)
            row = maze[next_space[1]]
            value = row[next_space[0]]
            logging.debug("Value: %s", value)
            maze = change_value(maze, next_space, visited_space)
            current_space = next_space
            path.append(current_space)
        cls()
    return print_maze(maze), path, count

maze_to_solve = [
    ["#","#","#","#","#","O","#","#","#"],
    ["#"," "," "," "," "," "," "," ","#"],
    ["#"," ","#","#","#","#","#"," ","#"],
    ["#"," ","#"," "," "," ","#"," ","#"],
    ["#"," ","#"," ","#"," ","#"," ","#"],
    ["#"," ","#"," ","#"," ","#"," ","#"],
    ["#"," ","#"," ","#"," ","#","#","#"],
    ["#"," "," "," "," "," "," "," ","#"],
    ["#","#","#","#","#","#","#","X","#"]
]

solved_paths = []
while True:
    print(f"Attempt Number: {count}")
    start_point = find_start_of_maze(maze_to_solve)
    failed = []
    solved_maze, solved_path, count = solve_maze(maze_to_solve, solved_paths, failed, start_point)
    solved_paths.append((solved_path, solved_maze))
    maze_to_solve = reset_maze(maze_to_solve)
    print(F"Solved Outside: {solved_paths}")

FIRST = True
for paths in solved_paths:
    if FIRST:
        smallest_path = paths
        FIRST = False
    if len(paths[0]) < len(smallest_path[0]):
        smallest_path = paths

print(smallest_path[1])
