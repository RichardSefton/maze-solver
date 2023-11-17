import maze_solver.generate as generate
from matplotlib.figure import Figure
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import json

#When given an image of a maze this script and functions will attempt to solve it. 

def solve_maze(maze):
    maze = generate.generate_maze(75, 75)
    # maze = np.where(maze == 1, 255, 0)
    # plt.figure()

    # img_buff = io.BytesIO()

    # img = make_image_from_maze(maze, 'maze.jpg', img_buff)

    # # image_array = np.asarray(img)
    explorer = Explorer(maze)
    print(explorer.maze)

    # maze = explorer.paint_start_end()
    # # new_img = make_image_from_copy(maze, 'maze_start_end.jpg')
    
    explorer.visited = explorer.explore_maze(explorer.entry_point, explorer.exit_point, {})

    explorer.solvable = explorer.determine_solvability()
    print(explorer.solvable)

    # img_buff.close()
    return

def make_image_from_copy(maze, filename):
    image = Image.fromarray(maze)
    image.save(filename)

def make_image_from_maze(maze, filename, img_buff):
    fig, ax = plt.subplots(figsize=(maze.shape[1], maze.shape[0]))
    ax.imshow(maze, cmap='gray')
    ax.axis('off')

    plt.savefig(img_buff, format='jpeg', bbox_inches='tight', pad_inches=0)
    img_buff.seek(0)
    img = Image.open(img_buff)
    img.save(filename)
    return img

class Explorer:
    entry_point = 0
    exit_point = 0
    maze = None
    visited = {}
    solvable = False

    def __init__(self, maze):
        self.maze = maze
        # self.calc_path_dimensions(maze)
        self.find_entry_point(maze)
        self.last_path_pos = self.entry_point
        self.find_exit_point(maze)
        

    def explore_maze(self, current_position, end_position, visited, node=None, intersects=None):
        row, col = current_position

        # Check if the current position is out of bounds or an obstacle
        if (
            row < 0
            or col < 0
            or row >= self.maze.shape[0]
            or col >= self.maze.shape[1]
            or self.maze[row, col] == 0  # Check for walls
        ):
            return {}
        
        #If the length of visisted is falsy, assume we're at the start of the maze
        if (node == None):
            node = {
                "start": (row, col),
                "end": None,
                "dir_x": True,
                "dir_y": False,
                "direction": 1,
                "dead_end": False,
                "children": [] 
            }

        # We need to see if this is a complete path.
        current_path = [current_position] 
        direction = None
        if (node["dir_x"]):
            direction = (row, col+node["direction"])
        if (node["dir_y"]):
            direction = (row+node["direction"], col)

        d_row, d_col = direction
        while (self.maze[row, col] == self.maze[min(d_row, self.maze.shape[0]-1), min(d_col, self.maze.shape[1]-1)]):
            if (d_row > self.maze.shape[0]-1 or d_col > self.maze.shape[1]-1): #We've exceeded the bounds of the maze
                break
            current_path.append(direction)
            node["end"] = [direction[0], direction[1]]
            direction = (d_row, d_col + node["direction"]) if node["dir_x"] else (d_row + node["direction"], d_col)
            d_row, d_col = direction

        current_path = np.array(current_path)

        if intersects == None:
            intersects = []

        intersects.append(current_path)

        # Split into separate arrays for x and y axes
        x_values = current_path[:, 0]  # Extract the x
        y_values = current_path[:, 1]  # Extract the y
        dir_x = np.all(x_values == x_values[0])
        dir_y = np.all(y_values == y_values[0])
        node["dir_x"] = dir_x
        node["dir_y"] = dir_y

        def exists_in_intersect(step):
            for intersect in intersects:
                intersect = intersect.tolist()
                if step in intersect:
                    return True
            return False

        children = []
        for step in current_path:
            if dir_x:
                if (self.maze[step[0]-1, step[1]] == 255 and not exists_in_intersect([step[0]-1, step[1]])):
                    children.append({ "start": step, "end": None, "dir_x": False, "dir_y": True, "direction": -1, "dead_end": False, "children": []})
                if (self.maze[step[0]+1, step[1]] == 255 and not exists_in_intersect([step[0]+1, step[1]])):
                    children.append({ "start": step, "end": None, "dir_x": False, "dir_y": True, "direction": 1, "dead_end": False, "children": []})
            if dir_y:
                if (self.maze[step[0], step[1]-1] == 255 and not exists_in_intersect([step[0], step[1]-1])):
                    children.append({ "start": step, "end": None, "dir_x": True, "dir_y": False, "direction": -1, "dead_end": False, "children": []})
                if (self.maze[step[0], step[1]+1] == 255 and not exists_in_intersect([step[0], step[1]+1])):
                    children.append({ "start": step, "end": None, "dir_x": True, "dir_y": False, "direction": 1, "dead_end": False, "children": []})
        node["children"] = children
    

        if not len(children):
            node["dead_end"] = not np.any(np.all(np.array(node["end"]) == np.array(self.exit_point)))
        

        for child in children:
            child = self.explore_maze(child["start"], child["end"], visited, child, intersects)

        return node
    
    def determine_solvability(self):
        solvable_paths = []
        curr_path = []
        def solvable(node):
            curr_path.append(np.array(node["start"]))
            if len(node["children"]) == 0:
                if not node["dead_end"]:
                    solvable_paths.append(curr_path.copy())
                    curr_path.clear() #reset the curr path array incase theres more than one road paved with gold
            else:
                for child in node["children"]:
                    solvable(child)
        solvable(self.visited)
        return solvable_paths     
        
    def find_entry_point(self, maze):
        height, width = maze.shape
        for h in range(height):
            if self.maze[h, 0] == 255:
                entry_point = h
        self.entry_point = [entry_point, 0]

    def find_exit_point(self, maze):
        height, width = maze.shape
        for h in range(height):
            if self.maze[h, -1] == 255:
                exit_point = h
        self.exit_point = [exit_point, width-1]


solve_maze([])





