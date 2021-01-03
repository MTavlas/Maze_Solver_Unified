from skimage import io
import numpy as np
import sys
from PIL import Image as im
from a_star_pathfinding import Node, astar

np.set_printoptions(threshold=sys.maxsize, linewidth=500)


class Img_process:

    def __init__(self, maze_dir):
        self.maze_dir = maze_dir
        self.maze = io.imread(self.maze_dir, as_gray=True)

    def condense(self, want_ends=True):
        condensed = []
        length = int(self.maze.size ** 0.5)
        for j in range(0, length, 8):
            row = []
            for i in range(0, length, 8):
                row.append(self.maze[j, i])
            condensed.append(row)
        self.maze_condensed = np.array(condensed)
        self.height = len(self.maze_condensed) - 1

        if want_ends:
            self.maze_condensed[0] = np.where(self.maze_condensed[0] == 1, 2, self.maze_condensed[0])
            self.maze_condensed[self.height] = np.where(self.maze_condensed[self.height] == 1, 3,
                                                        self.maze_condensed[self.height])
            return self.maze_condensed

        self.start = (np.where(self.maze_condensed == 1)[0][0],np.where(self.maze_condensed == 1)[1][0])
        self.end = (np.where(self.maze_condensed == 1)[0][-1],np.where(self.maze_condensed == 1)[1][-1])
        return self.maze_condensed, self.start, self.end


def change_1_to_0(maze_rev):
    maze_rev = np.where(maze_rev == 0, 5, maze_rev)
    maze_rev = np.where(maze_rev == 1, 0, maze_rev)
    maze_rev = np.where(maze_rev == 5, 1, maze_rev)
    return maze_rev

def change_0_to_1(maze_rev):
    maze_rev = np.where(maze_rev == 0, 5, maze_rev)
    maze_rev = np.where(maze_rev == 1, 0, maze_rev)
    maze_rev = np.where(maze_rev == 5, 1, maze_rev)
    return maze_rev


class Solver:

    def __init__(self, maze):
        self.maze = maze

        y_start, x_start = np.where(self.maze == 2)
        self.start_y = int(y_start)
        self.start_x = int(x_start)

    def check_neigbours(self, y, x):
        # current_pos = self.maze[x, y]

        try:
            upper_neighbour = self.maze[y - 1, x]
        except IndexError:
            upper_neighbour = None

        try:
            lower_neighbour = self.maze[y + 1, x]
        except IndexError:
            lower_neighbour = None

        try:
            right_neighbour = self.maze[y, x + 1]
        except IndexError:
            right_neighbour = None

        try:
            left_neighbour = self.maze[y, x - 1]
        except IndexError:
            left_neighbour = None

        if y == 0:
            upper_neighbour = None

        if x == 0:
            left_neighbour = None

        return [upper_neighbour, lower_neighbour, right_neighbour, left_neighbour]

    def move_forward(self):
        current_pos = (self.start_y, self.start_x)
        fork_pos = []
        while True:
            try:
                for i in range(self.maze.size):
                    current_neigh = self.check_neigbours(current_pos[0], current_pos[1])
                    self.maze[current_pos[0], current_pos[1]] = 9
                    if 1 in current_neigh:
                        if current_neigh.count(1) > 1:
                            fork_pos.append(current_pos)
                        move_dir = current_neigh.index(1)
                        if move_dir == 0:
                            current_pos = (current_pos[0] - 1, current_pos[1])
                        elif move_dir == 1:
                            current_pos = (current_pos[0] + 1, current_pos[1])
                        elif move_dir == 2:
                            current_pos = (current_pos[0], current_pos[1] + 1)
                        elif move_dir == 3:
                            current_pos = (current_pos[0], current_pos[1] - 1)
                    elif 3 in current_neigh:
                        print("I found the solution!")
                        print(self.maze)
                        print(f"It took me {i + 1} steps in total!")
                        break
                    else:
                        current_pos = fork_pos[0]
                        fork_pos.pop(0)
                break
            except IndexError:
                print(f"Could not find a solution to the maze after taking {i + 1} steps!")
                print(self.maze)
                break
        return self.maze


class To_image:

    def __init__(self, solved_maze):
        self.solved_maze = solved_maze

    def paintit(self):
        self.solved_maze = np.where(self.solved_maze == 1, 255, self.solved_maze)
        self.solved_maze = np.where(self.solved_maze == 9, 120, self.solved_maze)
        self.solved_maze = np.where(self.solved_maze == 3, 120, self.solved_maze)
        data = im.fromarray(self.solved_maze)
        data = data.convert("RGB")
        data.save("solution.png")


while True:
    try:
        maze_pic = Img_process(r"YOUR OWN PATH HERE")
        break
    except FileNotFoundError:
        maze_pic = Img_process(r"C:\Users\Memo\Desktop\Python\Projects\Maze_IMG_Process\maze50x50.png")
        break

"""
maze_to_be_solved = maze_pic.condense(True) 
maze_solved = Solver(maze_to_be_solved).move_forward()
To_image(maze_solved).paintit()

# For just finding if a path is possible and painting it
"""



maze_to_be_solved_astar, astar_start, astar_end = maze_pic.condense(False)  # For A* pathfinding

maze_inv = change_1_to_0(maze_to_be_solved_astar) # Change 1s to 0s for pathfinding algorithm

path, maze_solved_astar = astar(maze_inv,astar_start,astar_end) # Gives both the path in coordinates and the solved maze with number "9" replacing passed positions

maze_solved_astar = change_0_to_1(maze_solved_astar) # Changes back to reverse mode for image drawing.

To_image(maze_solved_astar).paintit() # Draws it
