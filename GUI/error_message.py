import tkinter as tk
from tkinter import filedialog
from Algs import control
import random
from Algs import pathcontrol

def show(message):
    root = tk.Tk()
    
    root.title("Select Nodes")
    root.geometry("240x240")
    
    label = tk.Label(root, text=message).pack()
    
    root.mainloop()
