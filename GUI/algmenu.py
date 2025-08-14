import tkinter as tk
from tkinter import filedialog
from Algs import control
import random
from Algs import pathcontrol
from GUI import error_message
def show_route(origin, destination, amount, G, selection, positions, degree):
    origin = int(origin)
    destination = int(destination)
    if origin <1 or origin > amount or destination < 1 or destination > amount:
        error_message.show("One or both nodes do not exist")
        
    pathcontrol.build_path(G, origin, destination, selection, positions, degree)
    

def show(amount, G, selection, degree, positions):
    root = tk.Tk()
    
    root.title("Select Nodes")
    root.geometry("240x300")
    frame1 = tk.Frame(root)
    plabel = tk.Label(frame1, text="Choose starting node").pack()
    choosep = tk.Entry(frame1)
    choosep.pack()
    qlabel = tk.Label(frame1, text="Choose destination").pack()
    chooseq = tk.Entry(frame1)
    chooseq.pack()
    routeButton = tk.Button(frame1, text="See route", command= lambda:show_route(choosep.get(), chooseq.get(), amount, G, selection, positions, degree)).pack()
    frame1.pack()
    root.mainloop()
