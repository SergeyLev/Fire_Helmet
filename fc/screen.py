from collections import namedtuple

import tkinter as tk


class Screen:
    resolution = namedtuple('Screen', ['width', 'height'])

    def __init__(self):
        root = tk.Tk()

        self.resolution.width = root.winfo_screenwidth()
        self.resolution.height = root.winfo_screenheight()
        root.destroy()
