from tkinter import *
from maze_solver.generate import generate

class GUI:
    height = 800
    width = 800
    title = "Maze Solver"
    root = None

    def __init__(self):
        return
        #do nothing

    def draw(self):
        self.root = Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")
        self.draw_menus()
        self.root.mainloop()

    def draw_menus(self):
        if (self.root == None):
            return

        menu_bar = Menu(self.root)
        maze_menu = Menu(menu_bar, tearoff=0)
        maze_menu.add_command(label="Generate Maze", command=generate.generate_maze_action)

        menu_bar.add_cascade(label="Maze", menu=maze_menu)

        self.root.config(menu=menu_bar)
