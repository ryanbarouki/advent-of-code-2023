import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce

with open('input.txt') as f:
    G = nx.Graph()
    edge_labels = {}
    for line in f:
        parent, children = line.strip().split(':')
        children = children.strip().split()
        for child in children:
            G.add_edge(parent, child)
            edge_labels[(parent, child)] = f"{parent}-{child}"
    #nx.draw(G)
    #pos = nx.spring_layout(G)
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    #plt.show()
    # LOL this feels like cheating but it's Christmas Day I don't care!
    # remove edges qqh-xbl, dsr-xzn, tbq-qfj
    G.remove_edge('qqh', 'xbl')
    G.remove_edge('dsr', 'xzn')
    G.remove_edge('tbq', 'qfj')
    print(reduce(lambda a,b: a*b, [len(c) for c in nx.connected_components(G)]))
