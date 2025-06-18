import tkinter as tk
from tkinter import filedialog
from Algs import control
import random


        

    
# This is the function that prompts the user to upload a file
def get_file(selection, degree=4):
    # Just doing some basic error avoidance
    fixedDeg = ["Half Theta-6","None", "Delaunay", "Degree 12 spanner"]
    if not selection in fixedDeg:
        degree = int(degree)
    # Get the file
    path = filedialog.askopenfilename()
    if path:
        control.openFile(path, selection, degree)
    
# This function sets up the build function, does not ask for a file because it was indicated that the user would like random points
def get_random(selection, degree=4, amount = 10):
    fixedDeg = ["Half Theta-6","None", "Delaunay", "Degree 12 spanner"]
    if not selection in fixedDeg:
        degree = int(degree)
    random = True
    # Number of nodes to be graphed
    amount = int(amount) if not amount == '' else 10
    control.build(selection, degree, random, amount)

# This toggles some of the visual elements on screen, specifically the fields that ask for the number of nodes to be randomly produced
def randomtoggle(var, submitBtn, nodeLabel, nodeField,frame1, frame2, typeList, conebox):
    if var.get():
        submitBtn.config(command=lambda: get_random(typeList.get(typeList.curselection()[0]), conebox.get(), nodeField.get()))
        nodeLabel.pack()
        nodeField.pack()
        frame1.pack_forget()
        frame2.pack()
        frame1.pack()
    else:
        submitBtn.config(command=lambda:get_file(typeList.get(typeList.curselection()[0]), conebox.get()))
        nodeLabel.pack_forget()
        nodeField.pack_forget()
        frame2.pack_forget()
    
    


def main():
    # This is just checking the value of the selected element of the listbox. Depending on the selection, a cone field will be visible. This is another sort of toggle
    def checkVal(event):
        needDeg = ["Yao","Theta","Ordered Theta"]
        listbox = event.widget
        selection = listbox.get(listbox.curselection())
        if selection in needDeg:
            frame.pack_forget()
            coneFrame.pack()
            frame.pack()
        else:
            coneFrame.pack_forget()
        
    # Building the root of the GUI
    root = tk.Tk()
    root.title("Building Graphs")
    root.geometry("240x300")
    
    # The following are all GUI elements
    
    nodefileLabel = tk.Label(root, text="Upload node file and Build Graph")
    
    
    listlabel = tk.Label(root, text="Choose the type of graph")
    typeList = tk.Listbox(root)
    typeList.insert(1, "None")
    typeList.insert(2, "Theta")
    typeList.insert(3, "Yao")
    typeList.insert(4,"Half Theta-6")
    typeList.insert(5,"Ordered Theta")
    typeList.insert(6, "Delaunay")
    typeList.insert(7, "Degree 12 spanner")
    typeList.config(height=3)
    typeList.bind("<<ListboxSelect>>",checkVal)
    typeList.selection_set(0)
    listlabel.pack()
    typeList.pack()
    nodefileLabel.pack()
    
    coneFrame = tk.Frame(root)
    
    coneLabel = tk.Label(coneFrame, text="Enter # of cones (Default 4)")
    coneLabel.pack()
    conebox = tk.Entry(coneFrame)
    conebox.pack()
    frame = tk.Frame(root, pady=20)
    var = tk.IntVar()
    submitBtn = tk.Button(frame, text="Build Graph", command=lambda: get_file(typeList.get(typeList.curselection()[0]), conebox.get()), bg="white", fg="black")
    frame2 = tk.Frame(root)
    nodeLabel = tk.Label(frame2, text="Enter number of nodes")
    nodeField = tk.Entry(frame2)
    randomCheckbtn = tk.Checkbutton(root, text="Random nodes?", variable=var, onvalue=1 , offvalue=0, command=lambda: randomtoggle(var, submitBtn, nodeLabel, nodeField, frame, frame2, typeList,conebox)).pack()
    
    submitBtn.pack()
    
    frame.pack()
    frame2.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
