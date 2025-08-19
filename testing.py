from pyvis.network import Network
from GUI import algmenu
import numpy as np
import math
import random

# G = Network(height='1000px', width='100%', notebook=True, directed=True,select_menu=True, filter_menu=True)

# G.add_node(1)
# G.add_node(2)
# G.add_edge(1,2)
# G.add_edge(2,1)
# print(G.edges)

rate = 1.15
startingamount = 230000
add = 10000

for i in range(45):
    startingamount = int(startingamount * 100) / 100
    print(f"Current balance: {startingamount} || Year: {i}")
    if not i == 0 and i % 10 == 0:
        add += 5000
    startingamount += add 
    startingamount *= rate


print(f"Ending portfolio balance: {startingamount}")