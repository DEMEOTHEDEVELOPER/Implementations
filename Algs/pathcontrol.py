from pyvis.network import Network
from GUI import algmenu
import numpy as np
import math
import random


def even(n):
    return n % 2 == 0

def height(u, t, d ,positions):
    if type(u) == int:
        ux,uy = positions[u-1]
        
    else:
        ux = u['x']
        uy = u['y']
    
    proj = projection(t, u, d)
    projx = proj[0]
    projy = proj[1]

    return abs(ux-projx) + abs(uy - projy)

    

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


def inCone(u, p, cone, angle):
    
    u = np.array([u['x'],u['y']])
    point = np.array([p['x'],p['y']])

    angleA = math.radians(cone * angle)
    angleB = math.radians((cone + 1) * angle)
    vecA = np.array([math.cos(angleA), math.sin(angleA)])
    vecB = np.array([math.cos(angleB), math.sin(angleB)])
    
    normA = vecA / np.linalg.norm(vecA)
    normB = vecB / np.linalg.norm(vecB)

    if not(np.cross(normA, point - u) >= 0 and np.cross(point - u, normB) >= 0 and np.dot(normA, point - u) >=0 and np.dot(normB, point - u) >=0):
        return False

    return True


def getEdge(fro, to, edges):
    
    for edge in edges:
        
        if edge['from'] == fro and edge['to'] == to:
            return edge

    return None

def getNeighbours(edges, u):
    return [edge['to'] for edge in edges if edge['from'] == u]
    

def Clean(u, t, N, d, angle):
    

    # Need to project the point onto the diagonal. If the point has a greater y than the projection then we know its cone 2 (0,1,2,3)
    
    cone = chooseCone(u, t, d)

    for neighbor in N:
        if not inCone(u, neighbor, cone, angle): 
            continue
        
        project = projection(t, neighbor, d)
        if (cone == 0 and project[0] < neighbor['x']) or (cone == 2 and project[0] > neighbor['x']):
            return True
        else:
            return False


def Greedy(u,t,N, angle):
    # First find the cone of u that contains t
    cone = None
    for i in range(4):
        if inCone(u, t, i, angle):
            cone = i 
            break
    
    #Next find the node that is in the same cone as t
    node = None
    for i in range(len(N)):
        if inCone(u, N[i], cone, angle):
            return N[i]

    return None 


def Sweep(u, t, N, d, angle):
    # Choose the cone in the direction of the diagonal
    cone = chooseCone(u, t, d)
    
    for i in range(len(N)):
        if inCone(u, N[i], cone, angle):
            return N[i]
        

    return None

def buildHTML(G, edgedist, eudist, pathlength):
    return f"""
        Edge Length:                {edgedist}
        Path Length:                {pathlength}
        Routing Ratio:              {(pathlength)/eudist}
        Euclidean distance (p->q):  {eudist}
        """


def buildPath(G, path, eudist, pathlength, positions):
    for i in path:
        
        edgedist = getEudist(i[0], i[1], positions)
        html = buildHTML(G, edgedist, eudist, pathlength)
        edge = getEdge(i[0], i[1], G.edges)
        
        G.edges.remove(edge)
        G.add_edge(i[0], i[1], color="#FF0000" if len(i) < 3 or i[2] == 'Sweep' else '#0000FF' , title=html, width=40)

def NextStep(u, t, N, d, angle):
    
    if Clean(u, t, N,d, angle):
        return (Greedy(u, t, N, angle), 'Greedy')

    else:
        return (Sweep(u, t, N, d, angle), 'Sweep')


def getEudist(origin, destination, positions=[]):
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

def routeTheta4(G, origin, destination, positions):
    angle=90
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
        u = NextStep(u, t, N, d, angle)
        # print(u)
        path.append((last['id'],u[0]['id'],u[1]))
        pathnodes.append(u[0]['id'])
        pathlength += getEudist(last['id'], u[0]['id'], positions)
        print(pathlength)
        u = u[0]
        
    buildPath(G, path, eudist, pathlength, positions)

    return pathlength
        


    
def case1(N, u , cone, angle):
    for i in range(len(N)):
        if inCone(u, N[i], cone, angle):
            return N[i]

    return None

def case2(N, t, cone, angle):
    for i in range(len(N)):
        if inCone(t, N[i], cone, angle):
            return N[i]

    return None
    


def routeHalfTheta6(G, origin, destination, positions):
    angle = 60
    eudist = getEudist(origin, destination, positions)
    pathlength = 0
    u = G.get_node(origin)
    t = G.get_node(destination)
    last = None
    path = []
    pathnodes = []
    pathnodes.append(u)

    while not u is t:
        
        found = False
        Nu = [G.get_node(node) for node in getNeighbours(G.edges, u['id'])]
        Nt = [G.get_node(node) for node in getNeighbours(G.edges, t['id'])]

        # The case of destination being in a positive cone of u
        for i in [0,2,4]:
            if inCone(u, t, i, angle):
                
                last = u
                cone = i
                u = case1(Nu, u, cone, angle)
                
                path.append((last['id'], u['id']))
                pathlength += getEudist(last, u) / 100
                print(pathlength)

                found = True
                break
        if found: continue 

        for i in [0,2,4]:
            if inCone(t,u,i, angle):
                last = t
                cone = i
                t = case2(Nt, t, cone, angle)
                path.append((last['id'], t['id']))
                pathlength += getEudist(last, t) / 100
                print(pathlength)
                found = True 
                break 
        if found: continue

        # The case of the destination being in a negative cone of u but zones 1 and 2 are both empty
    
    buildPath(G, path, eudist, pathlength, positions)

def chooseDiagonal(u, t, positions, angle):
    #Cone 0
    dpp = np.array([1,1])
    normdpp = dpp / np.linalg.norm(dpp)
    # Cone 1
    dpn = np.array([-1,-1])
    normdpn = dpn / np.linalg.norm(dpn)
    # Cone 2
    dnp = np.array([-1,1])
    normdnp = dnp / np.linalg.norm(dnp)
    # Cone 3
    dnn = np.array([1,-1])
    normdnn = dnn / np.linalg.norm(dnn)

    diagonals = [dpp, dnp, dpn,dnn]
    for cone in range(4):
        if inCone(t['id'] if type(t) == int else t, u['id'] if type(u) == int else u, cone, angle):
            return diagonals[cone]
    
    return None


def YaoSweep(p, t, N, d, angle):
    

    # figure out which cone faces the diagonal
    # if point is in an even cone of t, the diagonal will be in an odd cone of p
    # otherwise it will be in an even cone of p

    for i in range(4):
        if inCone(t, p, i, angle):
            cone = i
            break
        
    if even(cone):
        dcone = 0 if projection(t, p, d)[0] < p['x'] else 2
    else:
        dcone = 1 if projection(t, p, d)[0] > p['x'] else 3
    
    # Return the neighbour in that cone
    for node in N:
        if inCone(p, node, dcone, angle):
            return node 

    return None


def GreedySweep(G, p, t, d, positions, angle):
    N = [G.get_node(node) for node in getNeighbours(G.edges, p if type(p) == int else p['id'])]
    q = Greedy(p, t, N, angle)
    r = YaoSweep(p, t, N, d, angle)

    if r is None or getEudist(p, r, positions) > height(p, t, d, positions):
        return q
    else:
        return r

def routeYao(G, s, t, positions):
    eudist = getEudist(s, t, positions)
    angle = 360/4
    u = G.get_node(s)
    t = G.get_node(t)
    last = None
    path = []
    pathlength = 0
    nodes = []

    while not u is t:
        d = chooseDiagonal(u, t, positions, angle)
        last = u
        u = GreedySweep(G, u, t, d, positions, angle)
        path.append((last['id'], u['id']))
        pathlength += getEudist(last, u)
        print(u)
        if not u in nodes:
            nodes.append(u)
        else:
            nodes.append(u)
            break
    
    buildPath(G, path, eudist, pathlength/100, positions)
        



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
    elif selection.lower().startswith("half"):
        
        routeHalfTheta6(G, origin, destination, positions)
        G.show("Route.html", notebook=False)
    elif selection.lower().startswith("yao") and cones == 4:
        routeYao(G, origin, destination, positions)
        G.show("Route.html", notebook=False)
        
        
