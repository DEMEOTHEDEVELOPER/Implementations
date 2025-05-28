import networkx as nx
import pygraphviz as pg
import matplotlib.pyplot as plt
import sys
import math

# Placing the nodes onscreen
def drawNodes(G, nodes):
    positions = []
    xdata = []
    ydata = []
    curr = 1
    for node in nodes:
        node = node.strip("\n").split(",")
        x = float(node[0])
        y = float(node[1])
        
        while x in xdata:
            x += 0.000000000001
        xdata.append(x)
        
        while y in xdata:
            y += 0.000000000001
        ydata.append(y)
        G.add_node(curr, pos=(x,y))
        curr+=1
        positions.append((x,y))
    return positions

# 
def drawEdges(G, edges):
    for edge in edges:
        edge = edge.strip("\n").strip("\r").split(',')
        G.add_edge(float(edge[0]),float(edge[1]))
        
def drawYao4(G, positions):
    currnode = 1
    for i in positions:
        for cone in range(4):
            closest = None
            distance = float('inf')
            currcheck = 0
            
            for j in positions:
                currcheck +=1
                if currcheck == currnode:
                    continue
                xi, xj = (i[0], j[0])
                yi, yj = (i[1], j[1])
                
                if cone == 0:
                    if not xi < xj or not yi < yj:
                        continue
                    
                    node_distance = math.sqrt( ((xj-xi) ** 2) + ((yj - yi) **2))
                    if node_distance < distance:
                        closest = currcheck
                        distance = node_distance
                        
                if cone == 1:
                    
                    if not xj< xi or not yi < yj:
                        continue
                    
                    node_distance = math.sqrt( ((xi-xj) ** 2) + ((yj - yi) **2))
                    if node_distance < distance:
                        closest = currcheck
                        distance = node_distance
                        
                if cone == 2:
                    
                    if not xj< xi or not yj < yi:
                        continue
                    
                    node_distance = math.sqrt( ((xi-xj) ** 2) + ((yi - yj) **2))
                    if node_distance < distance:
                        closest = currcheck
                        distance = node_distance
                        
                if cone == 3:
                    
                    if not xi< xj or not yj < yi:
                        continue
                    
                    node_distance = math.sqrt( ((xj-xi) ** 2) + ((yi - yj) **2))
                    if node_distance < distance:
                        closest = currcheck
                        distance = node_distance
                        
            if not distance == float('inf'):
                G.add_edge(currnode, closest)
        currnode +=1
    

def drawTheta4(G, positions):
    print("Hello")


def main():
    #Make an empty graph
    G = nx.Graph()
    #import the nodes
    if (sys.argv[1] != "nodes.txt"):
        exit("nodes.txt not found after program filename\nTry - \"python3 something.py nodes.txt\"")
    f = open(sys.argv[1])
    nodes = f.readlines()
    
    positions = drawNodes(G, nodes)
    
    #if the user added an edges file
    if len(sys.argv)> 2:
        match sys.argv[2].lower():
            case "edges.txt":
                f = open(sys.argv[2])
                edges = f.readlines()
                drawEdges(G, edges)
            case "yao-4":
                drawYao4(G, positions)
                
        
        
    pos = nx.get_node_attributes(G,'pos')
    #plt.subplot(111)
    nx.draw(G, pos=pos, with_labels=False, node_size=5)
    plt.show()
    
    
if __name__=="__main__":
    main()
