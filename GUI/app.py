import tkinter as tk
from tkinter import filedialog
from Algs import control
import random


        

    

def get_file(selection, degree=4):
    
    if not (selection == "Half Theta-6" or selection == "None"):
        degree = int(degree)

    path = filedialog.askopenfilename()
    if path:
        control.openFile(path, selection, degree)
        
def get_random(selection, degree=4, amount = 10):
    random = True
    amount = int(amount) if not amount == '' else 10
    control.build(selection, degree, random, amount)

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

    def checkVal(event):
        listbox = event.widget
        selection = listbox.get(listbox.curselection())
        if selection == "Yao" or selection == "Theta":
            frame.pack_forget()
            coneFrame.pack()
            frame.pack()
        else:
            coneFrame.pack_forget()
        
    
    root = tk.Tk()
    root.title("Building Graphs")
    root.geometry("240x300")
    
    nodefileLabel = tk.Label(root, text="Upload node file and Build Graph")
    
    
    #uploadBtn = tk.Button(root, text = "Upload", command = get_file, bg="White", fg="black")
    #uploadBtn.pack()
    
    listlabel = tk.Label(root, text="Choose the type of graph")
    typeList = tk.Listbox(root)
    typeList.insert(1, "None")
    typeList.insert(2, "Theta")
    typeList.insert(3, "Yao")
    typeList.insert(4,"Half Theta-6")
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
