from pyvis.network import Network
from GUI import algmenu
import numpy as np
import math
import random

def build_path(G, origin, destination, selection, positions):
    originx, originy = positions[origin-1]
    destinationx, destinationy = positions[destination-1]
    
    eudist = math.sqrt(((destinationx-originx) **2)+((destinationy-originy) **2))

    if selection == "None":
        html = f"""
        Edge Length:         {eudist}
        Path Length:         {eudist}
        Routing Ratio:       {1}
        Euclidean distance:  {eudist}
        """
        G.add_edge(origin, destination, color = "#FF0000", title= html, width=40)
        G.show("Route.html", notebook=False)
        
