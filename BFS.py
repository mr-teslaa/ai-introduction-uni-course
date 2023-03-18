import argparse

def read_maze(file_path):
    with open(file_path, 'r') as file:
        maze = [[int(num) for num in line.split()] for line in file]
    return maze

def print_maze(maze):
    for row in maze:
        print(' '.join(str(cell) for cell in row))

def bfs(maze):
    start_node = (9, 7)
    goal_node = (0, 2)

    queue = [start_node]
    visited = set()
    parent = {start_node: None}

    while queue:
        current_node = queue.pop(0)

        if current_node == goal_node:
            break

        row, col = current_node
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]

        for neighbor in neighbors:
            n_row, n_col = neighbor
            if 0 <= n_row < 10 and 0 <= n_col < 10 and maze[n_row][n_col] == 0 and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current_node

    solution_path = []
    node = goal_node
    while node:
        solution_path.append(node)
        node = parent[node]
    solution_path.reverse()

    for row, col in visited:
        maze[row][col] = 2
    for row, col in solution_path:
        maze[row][col] = 5

    print_maze(maze)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find solution path for the maze using Breadth-first search algorithm.')
    parser.add_argument('file_path', type=str, help='Path to the maze file')
    args = parser.parse_args()

    maze = read_maze(args.file_path)
    bfs(maze)