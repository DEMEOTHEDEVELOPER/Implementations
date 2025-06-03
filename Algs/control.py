from pyvis.network import Network
from GUI import algmenu
import numpy as np
import math
import random
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
    currnode = 1
    angle = 360 / degree
    
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
            x += 0.000001
        xdata.append(x)
        
        while y in xdata:
            y += 0.000001
        ydata.append(y)
        G.add_node(curr, label=curr, x = (x* 100), y = -(y * 100), fixed=True)
        curr+=1
        positions.append((x,y))
    return positions

def randomNodes(G, amount):
    positions = []
    xdata = []
    ydata = []
    curr =1
    for i in range(amount):
        x = random.random() * 100
        y = random.random() * 100
        while x in xdata:
            x+= 0.00001
        while y in ydata:
            y+= 0.00001
        
        xdata.append(x)
        ydata.append(y)
        
        G.add_node(curr, label=curr, x = (x*100), y = -(y*100), fixed = True)
        curr +=1
        positions.append((x,y))
        
    return positions
        
        
def selectGraph(G, selection, degree, positions):
    match selection.lower():
        case "yao":
            drawYao(G, positions, degree)
        case "theta":
            drawTheta(G, positions, degree)
        case "half theta-6":
            drawTheta6(G, positions)

def build(selection, degree, amount = 10, nodes = ""):
    G = Network(height='1000px', width='100%', notebook=True)
    
    positions =  randomNodes(G, amount) if random else drawNodes(G, nodes)
    
    selectGraph(G, selection, degree, positions)
    
    G.show("Routing_Visualizer.html",notebook=False)
    algmenu.show(len(positions), G, selection, degree)
    
def openFile(filepath, selection, degree):
    file = open(filepath)
    nodes = file.readlines()
    build(selection, degree, nodes)
