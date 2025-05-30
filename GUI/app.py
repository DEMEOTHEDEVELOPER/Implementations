import tkinter as tk
from tkinter import filedialog
#from UnderstandingGViz import something
from Algs import control

    
def get_file(selection, degree):
    degree = int(degree)
    path = filedialog.askopenfilename()
    if path:
        control.openFile(path, selection, degree)
        


def main():
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
    listlabel.pack()
    typeList.pack()
    nodefileLabel.pack()
    
    coneLabel = tk.Label(root, text="Enter # of cones")
    coneLabel.pack()
    conebox = tk.Entry(root)
    conebox.pack()
    frame = tk.Frame(root, pady=20)
    submitBtn = tk.Button(frame, text="Build Graph", command=lambda: get_file(typeList.get(typeList.curselection()[0]), conebox.get()), bg="white", fg="black").pack()
    
    frame.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
