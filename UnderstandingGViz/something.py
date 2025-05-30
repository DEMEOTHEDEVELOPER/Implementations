import networkx as nx
import pygraphviz as pg
import matplotlib.pyplot as plt
import sys
import math
import numpy as np

def test():
    print(99)

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
    

def drawYao(G, positions, degree):
    angle = 360 / degree
    currnode = 1
    for i in positions:
        origin = np.array([i[0],i[1]])
        for cone in range(degree):
            
            closest = None
            distance = float('inf')
            currcheck = 0
            
            angleA = math.radians(cone * angle)
            angleB = math.radians((cone + 1) * angle)
            vecA = np.array([math.cos(angleA), math.sin(angleA)])
            vecB = np.array([math.cos(angleB), math.sin(angleB)])
            
            normA = vecA / np.linalg.norm(vecA)
            normB = vecB / np.linalg.norm(vecB)
            
            for j in positions:
                
                currcheck += 1
                
                if currnode == currcheck:
                    continue
                
                point = np.array([j[0],j[1]])
                
                if not(np.cross(normA, point - origin) >= 0 and np.cross(point - origin, normB) >= 0 and np.dot(normA, point - origin) >=0 and np.dot(normB, point - origin) >=0):
                    continue
                plot = point - origin
                currdist = math.sqrt(plot[0]**2 + plot[1]**2)
                if currdist < distance:
                    distance = currdist
                    closest = currcheck
            if not distance == float('inf'):
                G.add_edge(currnode, closest)
        currnode +=1


def drawTheta(G, positions, degree):
    angle = 360 / degree
    currnode = 1
    for i in positions:
        origin = np.array([i[0],i[1]])
        for cone in range(degree):
            
            closest = None
            distance = float('inf')
            currcheck = 0
            
            # Creating the cone and its bisector
            angleA = math.radians(cone * angle)
            angleB = math.radians((cone+1)*angle)
            vecA = np.array([math.cos(angleA), math.sin(angleA)])
            vecB = np.array([math.cos(angleB), math.sin(angleB)])
            
            normA = vecA / np.linalg.norm(vecA)
            normB = vecB / np.linalg.norm(vecB)
            
            bisector = normA + normB
            bisector /= np.linalg.norm(bisector)
            
            
            
            for j in positions:
                currcheck +=1
                #creating the point
                point = np.array([j[0], j[1]])
                # ensuring that we are not checking the origin against itself
                if currcheck == currnode:
                    continue
                
                # Checking to make sure that the point is within the cone
                if not(np.cross(normA, point - origin) >= 0 and np.cross(point - origin, normB) >= 0 and np.dot(normA, point - origin) >=0 and np.dot(normB, point - origin) >=0):
                    continue
                    
                # projecting the point onto the bisector 
                projection = np.dot(point - origin, bisector)
                
                if projection < distance:
                    
                    distance = projection
                    closest = currcheck
            if not distance == float('inf'):
                G.add_edge(currnode, closest)
                
                
        currnode+=1
        
def drawTheta6(G, positions):
    currnode = 1
    angle = 360 / 6
    for i in positions:
        origin = np.array([i[0],i[1]])
        for cone in [1,3,5]:
            closest = None
            distance = float('inf')
            currcheck = 0
            
            #Building the cone
            angleA = math.radians(cone * angle)
            angleB = math.radians((cone+1)*angle)
            vecA = np.array([math.cos(angleA), math.sin(angleA)])
            vecB = np.array([math.cos(angleB), math.sin(angleB)])
            
            normA = vecA / np.linalg.norm(vecA)
            normB = vecB / np.linalg.norm(vecB)
            
            bisector = normA + normB
            bisector /= np.linalg.norm(bisector)
            
            for j in positions:
                currcheck+=1
                
                point = np.array([j[0],j[1]])
                
                if currcheck ==currnode:
                    continue
                    
                if not(np.cross(normA, point - origin) >= 0 and np.cross(point - origin, normB) >= 0 and np.dot(normA, point - origin) >=0 and np.dot(normB, point - origin) >=0):
                    continue
                
                projection = np.dot(point - origin, bisector)
                
                if projection < distance:
                    
                    distance = projection
                    closest = currcheck
            if not distance == float('inf'):
                G.add_edge(currnode, closest)
                
                
        currnode+=1
                    
                    
def open_file(filepath, selection, degree):
    file = open(filepath)
    nodes = file.readlines()
    build(nodes, selection, degree)


def build(nodes, selection, degree):
    #Make an empty graph
    G = nx.Graph()
    
    
    positions = drawNodes(G, nodes)
    
    #if the user added an edges file
    
    match selection.lower():
        case "yao":
            drawYao(G, positions, degree)
        case "theta":
            drawTheta(G, positions, degree)
        case "half theta-6":
            drawTheta6(G, positions)
                
        
        
    pos = nx.get_node_attributes(G,'pos')
    nx.draw(G, pos=pos, with_labels=False, node_size=5)
    plt.show()
    
