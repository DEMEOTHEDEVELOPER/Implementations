import tkinter as tk
from tkinter import filedialog
from UnderstandingGViz import something

def buildGraph(root, nodes):
    
    something.build(nodes, selection)
    
def get_file(selection):
    path = filedialog.askopenfilename()
    if path:
        something.open_file(path, selection)
        
        
    
    

def main():
    root = tk.Tk()
    root.title("Building Graphs")
    root.geometry("200x500")
    
    nodefileLabel = tk.Label(root, text="Upload node file and Build Graph")
    
    
    #uploadBtn = tk.Button(root, text = "Upload", command = get_file, bg="White", fg="black")
    #uploadBtn.pack()
    
    listlabel = tk.Label(root, text="Choose the type of graph")
    typeList = tk.Listbox(root)
    typeList.insert(1, "None")
    typeList.insert(2, "Theta-4")
    typeList.insert(3, "Yao-4")
    typeList.config(height=3)
    listlabel.pack()
    typeList.pack()
    nodefileLabel.pack()
    
    submitBtn = tk.Button(root, text="Build Graph", command=lambda: get_file(typeList.get(typeList.curselection()[0])), bg="white", fg="black")
    
    submitBtn.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
