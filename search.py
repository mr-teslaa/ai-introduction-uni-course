import heapq
import argparse
import math
import sys

# Define command-line arguments
parser = argparse.ArgumentParser(description='Find a solution path for a given maze using various search algorithms.')
parser.add_argument('maze_file', type=str, help='Path to the maze file')
parser.add_argument('-d', '--dfs', action='store_true', help='Use depth-first search algorithm')
parser.add_argument('-b', '--bfs', action='store_true', help='Use breadth-first search algorithm')
parser.add_argument('-a', '--astar', action='store_true', help='Use A* search algorithm')
args = parser.parse_args()


# Define the directions in which we can move
directions = {
    "up": (-1, 0),
    "right": (0, 1),
    "down": (1, 0),
    "left": (0, -1),
}


maze = []
with open(args.maze_file) as f:
    for line in f:
        maze.append([int(x) for x in line.strip().split()])


# Define a helper function to get the neighbors of a cell
def get_neighbors(cell):
    neighbors = []
    for direction in directions.values():
        neighbor = (cell[0] + direction[0], cell[1] + direction[1])
        if (
            0 <= neighbor[0] < len(maze)
            and 0 <= neighbor[1] < len(maze[0])
            and maze[neighbor[0]][neighbor[1]] == 0
        ):
            neighbors.append(neighbor)
    return neighbors


# ================================
# START - Breadth-first search
# ================================
def bfs(start):
    queue = [start]  # initialize the queue with the starting cell
    parent = {}  # initialize the parent dictionary
    parent[start] = None  # the starting cell has no parent
    while queue:
        cell = queue.pop(0)
        maze[cell[0]][cell[1]] = 2  # mark the cell as visited
        if cell[0] == 0:
            # backtrack from the top to the starting cell and mark the cells on the path with value 5
            path = []
            while cell is not None:
                path.append(cell)
                cell = parent[cell]
            path.reverse()
            for p in path:
                maze[p[0]][p[1]] = 5
            return True  # we have found a path to the top of the maze
        for neighbor in get_neighbors(cell):
            if neighbor not in parent:
                queue.append(neighbor)  # add the neighbor to the queue
                parent[neighbor] = cell  # set the parent of the neighbor to the current cell
    return False  # we have not found a path to the top of the maze


# ================================
# END - Breadth-first search
# ================================



# ================================
# START - Depth-first search
# ================================
def dfs(cell):
    maze[cell[0]][cell[1]] = 2  # mark the cell as visited
    if cell[0] == 0:
        return True  # we have reached the top of the maze
    for neighbor in get_neighbors(cell):
        if dfs(neighbor):
            maze[neighbor[0]][neighbor[1]] = 5  # mark the cell as part of the solution path
            return True  # we have found a path to the top of the maze
    return False  # we have not found a path to the top of the maze

# ================================
# END - Depth-first search
# ================================


# ================================
# START - A* search algorithm
# ================================
def heuristic(cell):
    # Manhattan distance heuristic
    return abs(cell[0]) + abs(cell[1])

def astar(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    while frontier:
        current = heapq.heappop(frontier)[1]
        if current == goal:
            # backtrack from the goal to the starting cell and mark the cells on the path with value 5
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            for p in path:
                maze[p[0]][p[1]] = 5
            return True  # we have found a path to the goal
        for next_cell in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                cost_so_far[next_cell] = new_cost
                priority = new_cost + heuristic(goal)
                heapq.heappush(frontier, (priority, next_cell))
                came_from[next_cell] = current
                maze[next_cell[0]][next_cell[1]] = 2  # mark the cell as visited
    return False  # we have not found a path to the goal


# ================================
# END - A* search algorithm
# ================================




if args.astar:
    # Find the entrance and exit points of the maze
    entrance = (0, maze[0].index(0))
    exit = (len(maze)-1, maze[len(maze)-1].index(0))
    # Run A* algorithm to find the path from entrance to exit
    if astar(entrance, exit):
        # Output the maze with the solution path
        for row in maze:
            print(" ".join(str(x) for x in row))
    else:
        print("No path found")


elif args.bfs:
    # Start BFS from the entrance of the maze
    bfs((len(maze)-1, maze[len(maze)-1].index(0)))
    # Output the maze with the solution path
    for row in maze:
        print(" ".join(str(x) for x in row))

elif args.dfs:
    # Start DFS from the entrance of the maze
    dfs((len(maze)-1, maze[len(maze)-1].index(0)))

    # Output the maze with the solution path
    for row in maze:
        print(" ".join(str(x) for x in row))

else:
    print('Error: no algorithm specified')