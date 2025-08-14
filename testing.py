from pyvis.network import Network
from GUI import algmenu
import numpy as np
import math
import random

G = Network(height='1000px', width='100%', notebook=True, directed=True,select_menu=True, filter_menu=True)

G.add_node(1)
G.add_node(2)
G.add_edge(1,2)
G.add_edge(2,1)
print(G.edges)