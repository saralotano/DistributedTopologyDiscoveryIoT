import operator
import networkx as nx
from matplotlib import pyplot as plt
from networkx import degree_centrality, closeness_centrality, betweenness_centrality, eigenvector_centrality

n = 100
m = 1
p = 0.1  # if m = 1 the value of p does not matter
s = 0

G = nx.powerlaw_cluster_graph(n, m, p, seed=s)
# [2, 7, 0, 45, 8, 15, 1, 18, 3, 4] RELAYED MESSAGE NODES

# METHOD 1: degree_centrality
dc = dict(sorted(degree_centrality(G).items(), key=operator.itemgetter(1), reverse=True))
sorted_degree_centrality = list(dc.keys())
print(sorted_degree_centrality)
print(dc)
# [3, 4, 1, 0, 15, 45, 2, 7, 8, 9]

color_map = []
i = 0
while i < len(sorted_degree_centrality):
    if i < 10:
        color_map.append('#641e16')
    elif 10 <= i < 30:
        color_map.append('#922b21')
    elif 30 <= i < 50:
        color_map.append('#c0392b')
    elif 50 <= i < 70:
        color_map.append('#c0392b')
    else:
        color_map.append('#f2d7d5')
    i += 1
pos = nx.spring_layout(G, seed=9)
nx.draw(G, pos, node_color=color_map, with_labels=True)
plt.show()


# METHOD 2: closeness_centrality
cc = dict(sorted(closeness_centrality(G).items(), key=operator.itemgetter(1), reverse=True))
sorted_closeness_centrality = list(cc.keys())
print(sorted_closeness_centrality)
print(cc)
# [0, 1, 3, 2, 4, 49, 78, 7, 43, 47]
color_map = []
i = 0
while i < len(sorted_degree_centrality):
    if i < 10:
        color_map.append('#154360')
    elif 10 <= i < 30:
        color_map.append('#1f618d')
    elif 30 <= i < 50:
        color_map.append('#2980b9')
    elif 50 <= i < 70:
        color_map.append('#7fb3d5')
    else:
        color_map.append('#d4e6f1')
    i += 1

pos = nx.spring_layout(G, seed=9)
nx.draw(G, pos, node_color=color_map, with_labels=True)
plt.show()

# METHOD 3: betweenness_centrality
bc = dict(sorted(betweenness_centrality(G).items(), key=operator.itemgetter(1), reverse=True))
sorted_betweenness_centrality = list(bc.keys())
print(sorted_betweenness_centrality)
print(bc)
# [0, 3, 1, 4, 2, 7, 8, 15, 45, 9]
color_map = []
i = 0
while i < len(sorted_degree_centrality):
    if i < 10:
        color_map.append('#145a32')
    elif 10 <= i < 30:
        color_map.append('#1e8449')
    elif 30 <= i < 50:
        color_map.append('#27ae60')
    elif 50 <= i < 70:
        color_map.append('#7dcea0')
    else:
        color_map.append('#d4efdf')
    i += 1

pos = nx.spring_layout(G, seed=9)
nx.draw(G, pos, node_color=color_map, with_labels=True)
plt.show()

# METHOD 4: eigenvector_centrality
ec = dict(sorted(eigenvector_centrality(G).items(), key=operator.itemgetter(1), reverse=True))
sorted_eigenvector_centrality = list(ec.keys())
print(sorted_eigenvector_centrality)
print(ec)
# [1, 4, 3, 0, 33, 9, 11, 28, 69, 2]
color_map = []
i = 0
while i < len(sorted_degree_centrality):
    if i < 10:
        color_map.append('#784212')
    elif 10 <= i < 30:
        color_map.append('#af601a')
    elif 30 <= i < 50:
        color_map.append('#e67e22')
    elif 50 <= i < 70:
        color_map.append('#f0b27a')
    else:
        color_map.append('#fae5d3')
    i += 1

pos = nx.spring_layout(G, seed=9)
nx.draw(G, pos, node_color=color_map, with_labels=True)
plt.show()
