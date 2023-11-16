from tkinter import *
from maze_solver.generate import generate
from .menu import make_menu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class GUI:
    height = 800
    width = 800
    title = "Maze Solver"
    root = None
    maze = np.zeros(shape=(20, 20), dtype=int)
    canvas = None

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
        menu_bar = make_menu(self.root, [
            {
                "label": "Maze",
                "commands": [
                    {
                        "label": "Generate Maze",
                        "callback": self.generate_maze_action
                    }
                ]
            }
        ])
        self.root.config(menu=menu_bar)

    def draw_maze(self):
        if (self.root == None):
            return
        #destroy the previous canvas
        if (self.canvas != None):
            self.canvas.get_tk_widget().destroy()

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.imshow(self.maze, cmap='gray')
        ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        ax.set_xticks([])
        ax.set_yticks([])

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(side=TOP, fill=BOTH, expand=1)
        self.root.mainloop()

    def generate_maze_action(self):
        self.maze = generate.generate_maze(75, 75)
        self.draw_maze()