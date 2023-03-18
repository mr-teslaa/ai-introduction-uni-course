import argparse
import heapq
import numpy as np


# Parse command-line arguments
parser = argparse.ArgumentParser(description='Solve a maze using different search algorithms.')
parser.add_argument('algorithm', choices=['dfs', 'bfs', 'astar'], help='Search algorithm to use')
parser.add_argument('maze_file', type=str, help='File path of the maze text file')
args = parser.parse_args()


# Define constants and helper functions
START = (9, 0)
END = (0, 9)
MOVES = [(-1, 0), (0, 1), (0, -1), (1, 0)]
MOVE_NAMES = ['up', 'right', 'left', 'down']
HEURISTIC = lambda x: np.sqrt((x[0]-END[0])**2 + (x[1]-END[1])**2)


# Load maze from file
maze = []
with open(args.maze_file, 'r') as f:
    for line in f:
        maze.append([int(c) for c in line.strip()])


# Define print_maze function
def print_maze(maze, path=None):
    for row in maze:
        for col in row:
            if col == 1:
                print('#', end='')
            elif col == 2:
                print('.', end='')
            elif col == 5:
                print('*', end='')
            else:
                print(' ', end='')
        print()
    print()

# Define search functions
def dfs(maze, start, end):
    stack = [start]
    visited = set()
    while stack:
        current = stack.pop()
        if current == end:
            return backtrack(maze, start, end, visited)
        if current not in visited:
            visited.add(current)
            for move, move_name in zip(MOVES, MOVE_NAMES):
                next_pos = tuple(np.add(current, move))
                if is_valid(next_pos, maze):
                    stack.append(next_pos)
    return None

def bfs(maze, start, end):
    queue = [start]
    visited = set()
    while queue:
        current = queue.pop(0)
        if current == end:
            return backtrack(maze, start, end, visited)
        if current not in visited:
            visited.add(current)
            for move, move_name in zip(MOVES, MOVE_NAMES):
                next_pos = tuple(np.add(current, move))
                if is_valid(next_pos, maze):
                    queue.append(next_pos)
    return None

def astar(maze, start, end):
    heap = [(HEURISTIC(start), start)]
    visited = set()
    while heap:
        _, current = heapq.heappop(heap)
        if current == end:
            return backtrack(maze, start, end, visited)
        if current not in visited:
            visited.add(current)
            for move, move_name in zip(MOVES, MOVE_NAMES):
                next_pos = tuple(np.add(current, move))
                if is_valid(next_pos, maze):
                    cost = 1 + HEURISTIC(next_pos)
                    heapq.heappush(heap, (cost, next_pos))
    return None

def is_valid(pos, maze):
    i, j = pos
    if i < 0 or i >= len(maze) or j < 0 or j >= len(maze[0]) or maze[i][j] == 1:
        return False
    return True

def backtrack(maze, start, end, visited):
    path = [end]
    current = end
    while current != start:
        for move, move_name in zip(MOVES, MOVE_NAMES):
            next_pos = tuple(np.add(current, move))
            if next_pos in visited and is_valid(next_pos, maze):
                path.append(next_pos)
                current = next_pos
                break
    path.reverse()
    return path


# Call search function based on chosen algorithm
if args.algorithm == 'dfs':
    path = dfs(maze, start, goal)
elif args.algorithm == 'bfs':
    path = bfs(maze, start, goal)
elif args.algorithm == 'astar':
    path = astar(maze, start, goal)


# Print the maze with the solution path
print_maze(maze, path)