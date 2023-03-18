import sys
import heapq

def read_maze_file(maze_file):
    with open(maze_file) as f:
        maze = [[int(num) for num in line.split()] for line in f]
    return maze

def get_neighbors(maze, node):
    neighbors = []
    x, y = node
    if x > 0 and maze[x-1][y] == 0:
        neighbors.append((x-1, y))
    if x < len(maze)-1 and maze[x+1][y] == 0:
        neighbors.append((x+1, y))
    if y > 0 and maze[x][y-1] == 0:
        neighbors.append((x, y-1))
    if y < len(maze)-1 and maze[x][y+1] == 0:
        neighbors.append((x, y+1))
    return neighbors

def heuristic(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def astar(maze, start, end):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == end:
            break

        for next in get_neighbors(maze, current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    for node in path:
        x, y = node
        maze[x][y] = 5

    return maze

if __name__ == '__main__':
    maze_file = sys.argv[1]
    maze = read_maze_file(maze_file)
    start = (9, 0)
    end = (0, 9)
    astar_path = astar(maze, start, end)
    for row in astar_path:
        print(row)
