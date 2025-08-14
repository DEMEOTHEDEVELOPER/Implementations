from pyvis.network import Network
from GUI import algmenu
import numpy as np
import math
import random


def chooseCone(u, t, d):
    point = projection(t, u, d)
    u = np.array([u['x'],u['y']])
    return 2 if u[0] > point[0] else 0




def projection(origin, point, vec):
    origin = np.array([origin['x'],origin['y']])
    
    point = np.array([point['x'],point['y']])
    newp = point - origin

    projection = np.dot(newp, vec)

    return origin + projection * vec


def inCone(u, p, cone):
    
    u = np.array([u['x'],u['y']])
    point = np.array([p['x'],p['y']])

    angleA = math.radians(cone * 90)
    angleB = math.radians((cone + 1) * 90)
    vecA = np.array([math.cos(angleA), math.sin(angleA)])
    vecB = np.array([math.cos(angleB), math.sin(angleB)])
    
    normA = vecA / np.linalg.norm(vecA)
    normB = vecB / np.linalg.norm(vecB)

    if not(np.cross(normA, point - u) >= 0 and np.cross(point - u, normB) >= 0 and np.dot(normA, point - u) >=0 and np.dot(normB, point - u) >=0):
        return False

    return True


def getEdge(fro, to, edges):
    for edge in edges:
        if edge['from'] is fro and edge['to'] is to:
            return edge

    return None

def getNeighbours(edges, u):
    return [edge['to'] for edge in edges if edge['from'] == u]
    

def Clean(u, t, N, d):
    

    # Need to project the point onto the diagonal. If the point has a greater y than the projection then we know its cone 2 (0,1,2,3)
    
    cone = chooseCone(u, t, d)

    for neighbor in N:
        if not inCone(u, neighbor, cone): 
            continue
        
        project = projection(t, neighbor, d)
        if (cone == 0 and project[0] < neighbor['x']) or (cone == 2 and project[0] > neighbor['x']):
            return True
        else:
            return False


def Greedy(u,t,N):
    # First find the cone of u that contains t
    cone = None
    for i in range(4):
        if inCone(u, t, i):
            cone = i 
            break
    
    #Next find the node that is in the same cone as t
    node = None
    for i in range(len(N)):
        if inCone(u, N[i], cone):
            return N[i]

    return None 


def Sweep(u, t, N, d):
    # Choose the cone in the direction of the diagonal
    cone = chooseCone(u, t, d)
    
    for i in range(len(N)):
        if inCone(u, N[i], cone):
            return N[i]
        

    return None

def NextStep(u, t, N, d):
    
    if Clean(u, t, N,d):
        return (Greedy(u, t, N), 'Greedy')

    else:
        return (Sweep(u, t, N, d), 'Sweep')

def routeTheta4(G, origin, destination, positions):
    d1 = np.array([1,-1])
    normdiag1 = d1 / np.linalg.norm(d1)
    d2 = np.array([-1,1])
    normdiag2 = d2 / np.linalg.norm(d2)
    eudist = getEudist(origin, destination, positions)
    pathlength = 0
    u = G.get_node(origin)
    t = G.get_node(destination)
    last = None
    path = []
    pathnodes = []
    pathnodes.append(u)
    
    while not u is t:    
        Nbs = getNeighbours(G.edges, u['id'])
        N = [G.get_node(node) for node in Nbs]
        last = u
        if u['y'] - t['y'] < 0:
            d = normdiag1
        else:
            d = normdiag2
        u = NextStep(u, t, N, d)
        print(u)
        path.append((last['id'],u[0]['id'],u[1]))
        pathnodes.append(u[0]['id'])
        pathlength += getEudist(last, u[0]['id'], positions)
        u = u[0]
        
    for i in path:
        print(i)
        edgedist = getEudist(i[0], i[1], positions)
        html = f"""
        Edge Length:                {edgedist}
        Path Length:                {pathlength/1000}
        Routing Ratio:              {(pathlength/1000)/eudist}
        Euclidean distance (p->q):  {eudist}
        """
        G.edges.remove(getEdge(i[0], i[1], G.edges))
        G.add_edge(i[0], i[1], color="#FF0000" if i[2] == 'Sweep' else '#0000FF' , title=html, width=40)

    return pathlength
        

def getEudist(origin, destination, positions):
    if type(origin) is int:
        originx, originy = positions[origin-1]
    else:
        originx = origin['x']
        originy = origin['y']

    if type(destination) is int:
        destinationx, destinationy = positions[destination-1]
    else:
        destinationx = destination['x']
        destinationy = destination['y']
    
    return math.sqrt(((destinationx-originx) **2)+((destinationy-originy) **2))

    

def build_path(G, origin, destination, selection, positions, cones):
    
    eudist = getEudist(origin, destination, positions)
    if selection == "None":
        html = f"""
        Edge Length:         {eudist}
        Path Length:         {eudist}
        Routing Ratio:       {1}
        Euclidean distance:  {eudist}
        """
        G.add_edge(origin, destination, color = "#FF0000", title= html, width=40)
        G.show("Route.html", notebook=False)
    elif selection == "Theta" and cones == 4:
        vals = routeTheta4(G, origin, destination, positions)
        G.show("Route.html", notebook=False)
        
        
