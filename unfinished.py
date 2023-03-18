import heapq
import argparse

# Define command-line arguments
parser = argparse.ArgumentParser(description='Find a solution path for a given maze using various search algorithms.')
parser.add_argument('-d', '--dfs', action='store_true', help='Use depth-first search algorithm')
parser.add_argument('-b', '--bfs', action='store_true', help='Use breadth-first search algorithm')
parser.add_argument('-a', '--astar', action='store_true', help='Use A* search algorithm')
args = parser.parse_args()

# Define maze as a 2D array
maze = []
with open('maze.txt', 'r') as f:
    for line in f:
        maze.append(list(map(int, line.split())))

# Define start and end points
start = (9, 0)
end = (0, 9)

# Define utility functions
def get_neighbors(point):
    neighbors = []
    x, y = point
    if x > 0 and maze[x-1][y] == 0:
        neighbors.append((x-1, y))
    if x < 9 and maze[x+1][y] == 0:
        neighbors.append((x+1, y))
    if y > 0 and maze[x][y-1] == 0:
        neighbors.append((x, y-1))
    if y < 9 and maze[x][y+1] == 0:
        neighbors.append((x, y+1))
    return neighbors

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# Define search algorithms
def dfs():
    stack = [start]
    visited = set()
    while stack:
        current = stack.pop()
        if current == end:
            return True
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                stack.append(neighbor)
                maze[neighbor[0]][neighbor[1]] = 2
        maze[current[0]][current[1]] = 5
    return False

def bfs():
    queue = [start]
    visited = set()
    while queue:
        current = queue.pop(0)
        if current == end:
            return True
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                queue.append(neighbor)
                maze[neighbor[0]][neighbor[1]] = 2
        maze[current[0]][current[1]] = 5
    return False

def astar():
    heap = [(distance(start, end), start)]
    visited = set()
    g_score = {start: 0}
    f_score = {start: distance(start, end)}
    while heap:
        current = heapq.heappop(heap)[1]
        if current == end:
            return True
        visited.add(current)
        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + distance(current, neighbor)
            if neighbor in g_score and tentative_g_score >= g_score[neighbor]:
                continue
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = tentative_g_score + distance(neighbor, end)
        if neighbor not in visited:
                heapq.heappush(heap, (f_score[neighbor], neighbor))
                maze[neighbor[0]][neighbor[1]] = 2
        maze[current[0]][current[1]] = 5
    return False

