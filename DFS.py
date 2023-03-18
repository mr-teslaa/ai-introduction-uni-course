import argparse

def read_maze(file_name):
    maze = []
    with open(file_name, 'r') as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            maze.append(row)
    return maze

def write_maze(maze):
    for row in maze:
        print(' '.join(str(x) for x in row))

def dfs(maze, start, end):
    visited = set()
    stack = [start]

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            return True

        if maze[x][y] != 0:
            continue

        maze[x][y] = 2
        visited.add((x, y))

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= len(maze) or ny < 0 or ny >= len(maze[0]):
                continue
            if maze[nx][ny] == 1:
                continue
            if (nx, ny) in visited:
                continue
            stack.append((nx, ny))

    return False

def dfs_solve(maze):
    start = (len(maze) - 1, maze[len(maze)-1].index(0))
    end = (0, maze[0].index(0))

    if dfs(maze, start, end):
        x, y = start
        path = [(x, y)]

        while (x, y) != end:
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= len(maze) or ny < 0 or ny >= len(maze[0]):
                    continue
                if maze[nx][ny] != 2:
                    continue
                path.append((nx, ny))
                x, y = nx, ny
                break

        for x, y in path:
            maze[x][y] = 5

        write_maze(maze)
    else:
        print("No solution found")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Depth-first search algorithm for maze solving.')
    parser.add_argument('maze_file', metavar='maze_file', type=str, help='the path of the maze file')
    args = parser.parse_args()

    maze = read_maze(args.maze_file)
    dfs_solve(maze)
