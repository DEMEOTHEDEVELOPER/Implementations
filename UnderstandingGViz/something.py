import networkx as nx
import pygraphviz as pg
import matplotlib.pyplot as plt
import sys


#G = nx.Graph()
#G.add_node(1, pos=(0,0))
#G.add_node(2, pos=(2,3))
#pos = nx.get_node_attributes(G, 'pos')
#plt.subplot(111)
#nx.draw(G, pos, with_labels=True, font_weight='bold')
#
#plt.show()

def drawNodes(G, nodes):
    curr = 1
    for node in nodes:
        node1 = node.strip("\n").split(",")
        G.add_node(curr, pos=(int(node1[0]),int(node1[1])))
        curr+=1
        
def drawEdges(G, edges):
    for edge in edges:
        edge = edge.strip("\n").split(',')
        G.add_edge(int(edge[0]),int(edge[1]))
    

def main():
    #Make an empty graph
    G = nx.Graph()
    #import the nodes
    if (sys.argv[1] != "nodes.txt"):
        exit("nodes.txt not found after program filename\nTry - \"python3 something.py nodes.txt\"")
    f = open(sys.argv[1])
    nodes = f.readlines()
    
    drawNodes(G, nodes)
    
    #if the user added an edges file
    if len(sys.argv)> 2 and sys.argv[2] == "edges.txt":
        f = open(sys.argv[2])
        edges = f.readlines()
        
        drawEdges(G, edges)
        
        
    pos = nx.get_node_attributes(G,'pos')
    #plt.subplot(111)
    nx.draw(G, pos=pos, with_labels=True)
    plt.show()
    
    
if __name__=="__main__":
    main()
