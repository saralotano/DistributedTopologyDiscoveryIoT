import csv
import operator

import networkx as nx
from matplotlib import pyplot as plt

centralNodes = {}
path = '../data/relayedMsgSources.csv'

with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:

        if int(row[1]) not in list(centralNodes.keys()):
            centralNodes[int(row[1])] = 1
        else:
            centralNodes[int(row[1])] += 1

csv_file.close()

print(centralNodes)
sorted_d = dict(sorted(centralNodes.items(), key=operator.itemgetter(1), reverse=True))
print(sorted_d)
sorted_list = list(sorted_d.keys())
print(sorted_list)

sorted_list = [2, 7, 0, 45, 8, 15, 1, 18, 3, 4]

# POWER LAW
m = 1
p = 0.1
s = 0
G = nx.powerlaw_cluster_graph(100, m, p, seed=s)

color_map = []
for node in G:
    if node in sorted_list:
        color_map.append('#f87c10')
    else:
        color_map.append('#1c74b4')
pos = nx.spring_layout(G, seed=9)
nx.draw(G, pos, node_color=color_map, with_labels=True)
plt.show()

z = 0
while z < len(G.nodes):
    if z in list(centralNodes.keys()):
        print("nodeID =", z, ", neighbors =", len(G.adj[z]))
    z += 1
