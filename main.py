import tkinter as tk
import sys

from interface.interface import CanvasApp

if __name__ == "__main__":
    root = tk.Tk()
    app = CanvasApp(root)
    root.mainloop()